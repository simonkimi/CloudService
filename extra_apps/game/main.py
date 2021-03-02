import time
from os import name

from explore.models import ExploreModel
from campaign.models import CampaignModel
from log import Log
from user.models import User, UserProfile
from .net_sender import NetSender, LoginPasswordException, ServerCloseException, NetWorkException
from .constant import CAMPAIGN_MAP
from operate.models import OperateModel
from repair.models import RepairModel
from pvp.models import PvpModel
from build_ship.models import BuildShipModel
from build_equipment.models import BuildEquipmentModel


class ExploreUser:
    def __init__(self):
        self.user_data = {}

        self.user_ship = {}
        self.user_equipment = {}

        self.unlock_ship = []
        self.unlock_equipment = []

        self.task_info = {}

        self.ship_num_top = 0
        self.equipment_top = 0


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

        self._check_build_equipment(100, 110, 120, 130)

    def _check_pvp(self, fleet, formats, night_fight):
        try:
            time.sleep(2)
            pvp_list = self.sender.pvp_get_list()
            for pvp_person in pvp_list['list']:
                if pvp_person['resultLevel'] != 0:
                    continue
                pvp_uid = pvp_person['uid']
                pvp_username = pvp_person['username']
                pvp_ship_name = [i["title"] for i in pvp_person['ships']]
                time.sleep(2)
                self.sender.pvp_spy(uid=pvp_uid, fleet=fleet)
                time.sleep(2)
                fight_data = self.sender.pvp_fight(uid=pvp_uid, fleet=fleet, formats=formats)
                time.sleep(10)
                if fight_data['warReport']['canDoNightWar'] == 1 and night_fight == 1:
                    result_data = self.sender.pvp_get_result(night_fight=1)
                    time.sleep(5)
                else:
                    result_data = self.sender.pvp_get_result(night_fight=0)
                result_level = result_data['warResult']['resultLevel']
                Log.i('_check_pvp', "演习:", pvp_username, result_level)
                PvpModel.objects.create(
                    user=self.user_base,
                    username=pvp_username,
                    uid=pvp_uid,
                    ships='||'.join(pvp_ship_name),
                    result=result_level
                )
        except NetWorkException as e:
            self._create_operate(user=self.user_base, desc=f'网络错误: {e.code}, 请求{e.url}时发生错误', desc_type=2)
        except Exception as e:
            self._create_operate(user=self.user_base, desc=f'演习出现错误: {str(e)}', desc_type=2)

    def _check_repair(self):
        try:
            # 出浴船只
            for repair_dock in self.user.user_data['repairDockVo']:
                if 'endTime' in repair_dock and repair_dock["endTime"] < time.time():
                    time.sleep(2)
                    data = self.sender.repair_complete(repair_dock["id"], repair_dock["shipId"])
                    if "repairDockVo" in data:
                        self.user.user_data["repairDockVo"] = data["repairDockVo"]
                    if "shipVO" in data:
                        self.user.user_ship[int(repair_dock["shipId"])] = data["shipVO"]
            # 获取需要泡澡船只
            repairing_data = [int(dock['shipId']) for dock in self.user.user_data["repairDockVo"] if
                              "shipId" in dock and dock["endTime"] > time.time()]
            wait_shower = []
            for ship_id, ship_data in self.user.user_ship.items():
                if ship_id in repairing_data:
                    continue
                if "fleet_id" in ship_data and int(ship_data["fleet_id"]) > 4:
                    continue
                if ship_data["battleProps"]["hp"] != ship_data["battlePropsMax"]["hp"]:
                    wait_shower.append(int(ship_data["id"]))

            for dock in self.user.user_data["repairDockVo"]:
                if dock["locked"] == 0 and "endTime" not in dock and len(wait_shower) > 0:
                    time.sleep(3)
                    self.sender.shower(wait_shower[0])
                    time.sleep(3)
                    self.sender.rubdown(wait_shower[0])
                    name = self.user.user_ship[int(wait_shower[0])]["title"]
                    RepairModel.objects.create(user=self.user_base, name=name)
                    del wait_shower[0]
                    Log.i('_check_repair', "泡澡&搓澡: " + self.user.user_ship[int(wait_shower[0])]["title"])
        except NetWorkException as e:
            self._create_operate(user=self.user_base, desc=f'网络错误: {e.code}, 请求{e.url}时发生错误', desc_type=2)
        except Exception as e:
            self._create_operate(user=self.user_base, desc=f'洗澡出现错误: {str(e)}', desc_type=2)

    def _check_campaign(self, maps, battle_format):
        try:
            while True:
                time.sleep(3)
                campaign_count = self.sender.get_campaign_data()
                if campaign_count['passInfo']['remainNum'] == 0:
                    break
                # 开始战役
                fleet_data = self.sender.campaign_get_fleet(maps=maps)
                valid_fleet = [int(i) for i in fleet_data['campaignLevelFleet'] if int(i) != 0]
                if len(valid_fleet) == 0:
                    self._create_operate(self.user_base, desc='无法获取战役队伍, 已关闭战役开关', desc_type=2)
                    self.user_profile.campaign_map = 0
                    self.user_profile.save(update_fields=['campaign_map'])
                    break
                self._fast_repair(valid_fleet)
                time.sleep(3)
                self.sender.supply(valid_fleet)
                time.sleep(3)
                self.sender.campaign_get_spy(maps=maps)
                time.sleep(2)
                campaign_data = self.sender.campaign_fight(maps, battle_format)
                time.sleep(10)
                campaign_result = self.sender.campaign_get_result(campaign_data['warReport']['canDoNightWar'])
                self._build_campaign_award(CAMPAIGN_MAP[str(maps)], campaign_result['newAward'])
                Log.i('_check_campaign', self.username, CAMPAIGN_MAP[str(maps)], "完成")
                for ship in campaign_result['shipVO']:
                    self.user.user_ship[ship['id']] = ship
        except NetWorkException as e:
            self._create_operate(user=self.user_base, desc=f'网络错误: {e.code}, 请求{e.url}时发生错误', desc_type=2)
        except Exception as e:
            self._create_operate(user=self.user_base, desc=f'战役出现错误: {str(e)}', desc_type=2)

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
                    if 'newAward' in explore_result and len(explore_result['newAward']) != 0:
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

    def _build_campaign_award(self, campaign_map, award):
        CampaignModel.objects.create(
            user=self.user_base,
            map=campaign_map,
            oil=award['2'] if '2' in award else 0,
            ammo=award['3'] if '3' in award else 0,
            steel=award['4'] if '4' in award else 0,
            aluminium=award['9'] if '9' in award else 0,
            fast_build=award['141'] if '141' in award else 0,
            build_map=award['241'] if '241' in award else 0,
            fast_repair=award['541'] if '541' in award else 0,
            equipment_map=award['741'] if '741' in award else 0,
        )

    def _fast_repair(self, fleet: [int]):
        user_ship = self.user.user_ship
        need_repair = [i for i in fleet if
                       user_ship[i]['battleProps']['hp'] * 4 < user_ship[i]['battlePropsMax']['hp']]

        if len(need_repair) != 0:
            time.sleep(3)
            repair_data = self.sender.instant_repair(ships=need_repair)
            # 更新船只信息
            if "shipVOs" in repair_data:
                for ship in repair_data['shipVOs']:
                    self.user.user_ship[ship['id']] = ship

    def _check_build_ship(self, oil, ammo, steel, aluminium):
        try:
            for dock in self.user.user_data['dockVo']:
                if len(self.user.user_ship) >= self.user.ship_num_top:
                    return True
                if dock['locked'] == 0:
                    if 'endTime' in dock:
                        if dock['endTime'] > time.time():
                            continue
                        time.sleep(3)
                        ship = self.sender.get_boat(dock['id'])
                        if is_new := ship['shipVO']['shipCid'] not in self.user.unlock_ship:
                            time.sleep(2)
                            self.sender.lock_ship(ship_id=ship['shipVO']['id'])
                        self.user.user_ship[int(ship['shipVO']['id'])] = ship['shipVO']
                        BuildShipModel.objects.create(
                            user=self.user_base,
                            name=ship['shipVO']['title'],
                            cid=ship['shipVO']['shipCid'],
                            is_new=is_new
                        )
                    time.sleep(3)
                    self.sender.build_boat(dock['id'], oil, ammo, steel, aluminium)
        except NetWorkException as e:
            self._create_operate(user=self.user_base, desc=f'网络错误: {e.code}, 请求{e.url}时发生错误', desc_type=2)
            return False
        except Exception as e:
            self._create_operate(user=self.user_base, desc=f'建造船只出现错误: {str(e)}', desc_type=2)
            return False

    def _check_build_equipment(self, oil, ammo, steel, aluminium):
        try:
            for dock in self.user.user_data['equipmentDockVo']:
                if sum([i['num'] for i in self.user.user_equipment.values()]) >= self.user.equipment_top:
                    return True
                if dock['locked'] == 0:
                    if 'endTime' in dock:
                        if dock['endTime'] > time.time():
                            continue
                        time.sleep(3)
                        equipment = self.sender.get_equipment(dock['id'])
                        self.user.user_equipment[int(equipment['equipmentVo']['equipmentCid'])] = equipment[
                            'equipmentVo']
                        BuildEquipmentModel.objects.create(
                            user=self.user_base,
                            cid=int(equipment['equipmentVo']['equipmentCid'])
                        )
                    time.sleep(3)
                    self.sender.build_equipment(dock['id'], oil, ammo, steel, aluminium)
        except NetWorkException as e:
            self._create_operate(user=self.user_base, desc=f'网络错误: {e.code}, 请求{e.url}时发生错误', desc_type=2)
            return False
        except Exception as e:
            self._create_operate(user=self.user_base, desc=f'开发装备出现错误: {str(e)}', desc_type=2)
            return False

    def _parse_user_data(self) -> bool:
        try:
            # 获取用户数据
            self.user.user_data = self.sender.get_user_data()
            if 'userVo' not in self.user.user_data:
                self._create_operate(user=self.user_base, desc=f'无法获取userVo, 可能绑错区, 自动关闭开关', desc_type=2)
                return False
            self.username = self.user.user_data["userVo"]["username"]
            self.user_profile.username = self.username
            self.user_profile.save(update_fields=['username'])
            Log.i('ParseUserData', "当前用户:", self.username, '登录成功')

            # 解析船只数据
            user_ship = self.sender.get_user_ship()
            self.user.user_ship.clear()
            for eachShip in user_ship['userShipVO']:
                self.user.user_ship[int(eachShip['id'])] = eachShip

            # 解析装备数据
            for equipment in self.user.user_data['equipmentVo']:
                self.user.user_equipment[int(equipment['equipmentCid'])] = equipment

            # 解析任务列表
            for eachTask in self.user.user_data['taskVo']:
                self.user.task_info[eachTask['taskCid']] = eachTask

            # 用户数据
            self.user.ship_num_top = self.user.user_data['userVo']['shipNumTop']
            self.user.equipment_top = self.user.user_data['userVo']['equipmentNumTop']

            self.user.unlock_ship = [int(i) for i in self.user.user_data['unlockShip']]

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
