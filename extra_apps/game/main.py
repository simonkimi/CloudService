import time

from explore.models import ExploreModel
from log import Log
from user.models import User, UserProfile
from .net_sender import NetSender, LoginPasswordException, ServerCloseException, NetWorkException
from operate.models import OperateModel


class ExploreUser:
    def __init__(self):
        self.user_ship = {}
        self.task_info = {}
        self.user_data = {}
        self.unlockShip = []
        self.shipNumTop = 0
        self.dock = []
        self.equipment_dock = []
        self.equipment_num = 0
        self.equipment_top = 0
        self.uid = None
        self.login_award = 0

        self.fleet = {
            0: [0, 0, 0, 0, 0, 0],
            1: [0, 0, 0, 0, 0, 0],
            2: [0, 0, 0, 0, 0, 0],
            3: [0, 0, 0, 0, 0, 0],
            4: [0, 0, 0, 0, 0, 0],
            5: [0, 0, 0, 0, 0, 0],
            6: [0, 0, 0, 0, 0, 0],
            7: [0, 0, 0, 0, 0, 0]
        }


class ExploreMain:
    def __init__(self, user: User):
        self.user = ExploreUser()
        self.user_base = user
        self.user_data = ExploreUser()
        self.user_profile = UserProfile.objects.get(user=user)
        self.username = None
        self.sender = NetSender(
            username=self.user_base.username,
            password=user.password.split('$', 1)[-1],
            server=self.user_profile.server
        )

    def main(self):
        # 登录游戏
        if not self.login():
            return
        if not self._parse_user_data():
            return

        self._check_explore()

    def _check_explore(self):
        last_explore_data = None
        try:
            # 检测远征
            for explore in self.user.user_data['pveExploreVo']['levels']:
                if 'fleetId' in explore:
                    explore_id: str = explore['exploreId']
                    fleet_id = explore['fleetId']
                    time.sleep(3)
                    explore_result = self.sender.get_explore(explore_id)

                    map_name = explore_id.replace('000', '-')
                    success = explore_result['bigSuccess']
                    Log.i("_check_explore", self.username, "远征", map_name, f'{"大" if success else ""}成功')
                    if 'newAward' in explore_result and len('newAward') != 0:
                        self._build_explore_award(map_name, success, explore_result['newAward'])
                    time.sleep(3)
                    rsp = self.sender.start_explore(maps=explore_id, fleet=fleet_id)
                    last_explore_data = rsp['pveExploreVo']['levels']
            # 检测最近上线时间
            if last_explore_data is None:
                last_explore_data = self.user.user_data['pveExploreVo']['levels']
            levels = sorted(last_explore_data, key=lambda x: x['endTime'])
            if len(levels) != 0:
                self.user_profile.next_time = levels[0]['endTime']
                self.user_profile.save(update_fields=['next_time'])
        except NetWorkException as e:
            self._create_operate(user=self.user_base, desc=f'网络错误: {e.code}, 请求{e.url}时发生错误', desc_type=2)
        except Exception as e:
            self._create_operate(user=self.user_base, desc=f'远征出现错误: {str(e)}', desc_type=2)
            return False

    def _build_explore_award(self, explore_map, success, award):
        ExploreModel.objects.create(
            user=self.user_base,
            map=explore_map,
            success=success,
            oil=award['2'] if '2' in award else 0,
            ammo=award['3'] if '3' in award else 0,
            steel=award['4'] if '4' in award else 0,
            aluminium=award['9'] if '9' in award else 0,
            fast_build=award['141'] if '141' in award else 0,
            build_map=award['241'] if '241' in award else 0,
            fast_repair=award['541'] if '541' in award else 0,
            equipment_map=award['741'] if '741' in award else 0,
        )

    def _parse_user_data(self) -> bool:
        try:
            # 获取用户数据
            self.user.user_data = self.sender.get_user_data()
            if 'userVo' not in self.user.user_data:
                self._create_operate(user=self.user_base, desc=f'无法获取userVo, 可能绑错区, 自动关闭开关', desc_type=2)
                return False
            self.username = self.user.user_data["userVo"]["username"]
            Log.i('ParseUserData', "当前用户:", self.username, '登录成功')

            # 解析船只数据
            user_ship = self.sender.get_user_ship()
            self.user.user_ship.clear()
            for eachShip in user_ship['userShipVO']:
                self.user.user_ship[int(eachShip['id'])] = eachShip

            # 解析任务列表
            for eachTask in self.user.user_data['taskVo']:
                self.user.task_info[eachTask['taskCid']] = eachTask

        except NetWorkException as e:
            self._create_operate(user=self.user_base, desc=f'网络错误: {e.code}, 请求{e.url}时发生错误', desc_type=2)
            return False
        except Exception as e:
            self._create_operate(user=self.user_base, desc=f'解析用户数据出现错误: {str(e)}', desc_type=2)
            return False

        return True

    def login(self) -> bool:
        self.user_profile.last_time = time.time()
        self.user_profile.save(update_fields=['last_time'])
        try:
            self.sender.login()
        except LoginPasswordException:
            self._create_operate(user=self.user_base, desc=f'用户名或密码错误, 无法登录服务器, 自动关闭开关', desc_type=2)
            self.user_profile.switch = False
            self.user_profile.save(update_fields=['switch'])
            return False
        except ServerCloseException:
            self._create_operate(user=self.user_base, desc=f'服务器维护中, 等待一个小时后再登录', desc_type=1)
            return False
        except Exception as e:
            self._create_operate(user=self.user_base, desc=f'登录失败: {str(e)}, 等待一个小时后再登录', desc_type=2)
            return False
        self._wait_one_hour()
        self._create_operate(user=self.user_base, desc=f'登录游戏, 准备开始任务', desc_type=0)
        return True

    def _create_operate(self, user, desc, desc_type):
        print('Operate', self.username or '未登录', self.user_profile.username, desc)
        OperateModel.objects.create(user=user, desc=desc, desc_type=desc_type)

    def _wait_one_hour(self):
        self.user_profile.next_time = int(time.time()) + 60 * 60
        self.user_profile.save(update_fields=['next_time'])
