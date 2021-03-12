import base64
import requests
import time
import hashlib
import datetime
import hmac
import json
import zlib
import random
from urllib.parse import urlencode
from extra_apps.log import Log
from extra_apps.game.constant import URL_IOS_VERSION, URL_VERSION, PASS_KEY, PASS_KEY_HEAD, SERVER_LIST, NORMAL_HEADERS
from user.models import UserProfile


class LoginPasswordException(Exception):
    pass


class ServerCloseException(Exception):
    pass


class NetWorkException(Exception):
    def __init__(self, code, url=""):
        self.code = code
        self.url = url


class NetSender:
    def __init__(self, username, password, server):
        self._is_login = False
        self._cookies = None
        self._version = None
        self._channel = None
        self._username = username
        self._password = password
        self._server_index = server
        self._server = SERVER_LIST[server]
        self._requests = requests.session()

        # self._requests.verify = False

    def get_user_data(self):
        url = f'{self._server}api/initGame?&crazy=0{self._build_url_tail()}'
        return self._build_get(url)

    def get_user_ship(self):
        url = f'{self._server}api/getShipList{self._build_url_tail()}'
        return self._build_get(url)

    def get_explore(self, maps):
        url = f'{self._server}explore/getResult/{maps}/{self._build_url_tail()}'
        return self._build_get(url)

    def start_explore(self, maps, fleet):
        url = f'{self._server}explore/start/{fleet}/{maps}/{self._build_url_tail()}'
        return self._build_get(url)

    def instant_repair(self, ships: [int]):
        url = f'{self._server}boat/instantRepairShips/[{",".join([str(i) for i in ships])}]/{self._build_url_tail()}'
        return self._build_get(url)

    def get_campaign_data(self):
        url = f'{self._server}campaign/getUserData/{self._build_url_tail()}'
        return self._build_get(url)

    def campaign_get_fleet(self, maps):
        url = f'{self._server}campaign/getFleet/{maps}/{self._build_url_tail()}'
        return self._build_get(url)

    def supply(self, ships):
        url = f'{self._server}boat/supplyBoats/[{",".join([str(x) for x in ships])}]/0/0/{self._build_url_tail()}'
        return self._build_get(url)

    def campaign_get_spy(self, maps):
        url = f'{self._server}campaign/spy/{maps}/{self._build_url_tail()}'
        return self._build_get(url)

    def campaign_fight(self, maps, battle_format):
        url = f'{self._server}campaign/challenge/{maps}/{battle_format}/{self._build_url_tail()}'
        return self._build_get(url)

    def campaign_get_result(self, night_fight):
        url = f'{self._server}campaign/getWarResult/{night_fight}/{self._build_url_tail()}'
        return self._build_get(url)

    def repair_complete(self, dock_id, ship_id):
        url = f'{self._server}boat/repairComplete/{dock_id}/{ship_id}/{self._build_url_tail()}'
        return self._build_get(url)

    def shower(self, ship_id):
        url = f'{self._server}boat/repair/{ship_id}/0/{self._build_url_tail()}'
        return self._build_get(url)

    def rubdown(self, ship_id):
        url = f'{self._server}boat/rubdown/{ship_id}{self._build_url_tail()}'
        return self._build_get(url)

    def get_login_award(self):
        url = f'{self._server}active/getLoginAward/c3ecc6250c89e88d83832e3395efb973/{self._build_url_tail()}'
        return self._build_get(url)

    def pvp_get_list(self):
        url = f'{self._server}pvp/getChallengeList/{self._build_url_tail()}'
        return self._build_get(url)

    def pvp_spy(self, uid, fleet):
        url = f'{self._server}pvp/spy/{uid}/{fleet}/{self._build_url_tail()}'
        return self._build_get(url)

    def pvp_fight(self, uid, fleet, formats):
        url = f'{self._server}pvp/challenge/{uid}/{fleet}/{formats}/{self._build_url_tail()}'
        return self._build_get(url)

    def pvp_get_result(self, night_fight):
        url = f'{self._server}pvp/getWarResult/{night_fight}/{self._build_url_tail()}'
        return self._build_get(url)

    def build_boat(self, dock, oil, ammo, steel, aluminium):
        url = f'{self._server}dock/buildBoat/{dock}/{oil}/{steel}/{ammo}/{aluminium}{self._build_url_tail()}'
        return self._build_get(url)

    def build_equipment(self, dock, oil, ammo, steel, aluminium):
        url = f'{self._server}dock/buildEquipment/{dock}/{oil}/{steel}/{ammo}/{aluminium}{self._build_url_tail()}'
        return self._build_get(url)

    def get_boat(self, dock):
        url = f'{self._server}dock/getBoat/{dock}/{self._build_url_tail()}'
        return self._build_get(url)

    def get_equipment(self, dock):
        url = f'{self._server}dock/getEquipment/{dock}/{self._build_url_tail()}'
        return self._build_get(url)

    def lock_ship(self, ship_id):
        url = f'{self._server}boat/lock/{ship_id}/{self._build_url_tail()}'
        return self._build_get(url)

    def login_award(self):
        url = f'{self._server}active/getLoginAward/c3ecc6250c89e88d83832e3395efb973/{self._build_url_tail()}'
        return self._build_get(url)

    def get_task(self, cid):
        url = f'{self._server}task/getAward/{cid}/{self._build_url_tail()}'
        return self._build_get(url)

    def _build_get(self, url):
        try:
            data = self._requests.get(url=url, cookies=self._cookies, headers=NORMAL_HEADERS, timeout=20).content
            if data[0] == 0x78 and data[1] == 0xDA:
                data = zlib.decompress(data)
            json_data = json.loads(data)
            if 'eid' in json_data:
                raise NetWorkException(code=json_data['eid'], url=url)
            return json_data
        except Exception as e:
            raise Exception(f'{str(url)}, {str(e)}')

    def login(self, user_profile: UserProfile = None):
        saved_token = user_profile.token if user_profile is not None else ''
        if self._is_login:
            return
        need_refresh_token = False
        uid = None
        url_version = URL_VERSION if self._server_index <= 3 else URL_IOS_VERSION
        self._channel = '100011' if self._server_index <= 3 else '100015'
        # 获取版本信息
        try:
            rep = self._requests.get(url=url_version).json()
            if 'version' not in rep:
                raise ServerCloseException('服务器维护中...')
            self._version = rep['version']['newVersionId']
            login_server = rep['loginServer']
            hm_login_server = rep['hmLoginServer']
        except Exception as e:
            Log.e('NetSender.login.version', '获取Version出错', f'用户名:{self._username}', str(e))
            raise Exception('NetSender.login.version ' + str(e))

        while True:
            if len(saved_token) != 32 or need_refresh_token:
                # 获取token
                try:
                    url_token = f'{hm_login_server}1.0/get/login/@self'
                    login_data = json.dumps({
                        "platform": "0",
                        "appid": "0",
                        "app_server_type": "0",
                        "password": self._password,
                        "username": self._username
                    }).replace(" ", "")
                    rsp = self._requests.post(url=url_token, data=login_data,
                                              headers=self._build_headers(url_token)).json()
                    if "error" in rsp and int(rsp["error"]) != 0:
                        if int(rsp['error']) == 21003:
                            raise LoginPasswordException()
                        raise Exception(f'code:{rsp["error"]} msg:{rsp["errmsg"] if "errmsg" in rsp else ""}')
                    saved_token = rsp['access_token']
                except Exception as e:
                    Log.e('NetSender.login.token', '获取Token出错', f'用户名:{self._username}', str(e))
                    raise Exception('NetSender.login.token ' + str(e))

                # 验证token并获取游戏token
                try:
                    url_info = f'{hm_login_server}1.0/get/userInfo/@self'
                    data = json.dumps({"access_token": saved_token})
                    rsp = self._requests.post(url=url_token, data=data, headers=self._build_headers(url_info)).json()
                    if "error" in rsp and int(rsp["error"]) != 0:
                        raise Exception(f'验证Token出错:{rsp["errmsg"]}')
                    if user_profile is not None:
                        user_profile.token = saved_token
                        user_profile.save(update_fields=['token'])
                except Exception as e:
                    Log.e('NetSender.login.url_info)', '验证Token出错', f'用户名:{self._username}', str(e))
                    raise Exception('NetSender.login.url_info ' + str(e))

            # 获取用户Cookies
            try:
                url_login = f'{login_server}index/hmLogin/{saved_token}{self._build_url_tail()}'
                rsp = self._requests.get(url=url_login)
                login_data = json.loads(zlib.decompress(rsp.content))
                if 'eid' in login_data and int(login_data['eid']) == -127:
                    if not need_refresh_token:
                        need_refresh_token = True
                        continue
                    Log.e('NetSender.login.url_login)', '获取Token出错', f'用户名:{self._username}', '两次获取Token均出现-127问题')
                    raise Exception('NetSender.login.url_login 两次获取Token均出现-127问题')

                self._cookies = rsp.cookies.get_dict()
                rsp_data = json.loads(zlib.decompress(rsp.content))
                uid = rsp_data['userId']
                break
            except Exception as e:
                Log.e('NetSender.login.url_login)', '获取Token出错', f'用户名:{self._username}', str(e))
                raise Exception('NetSender.login.url_login ' + str(e))

        # 正式登录游戏
        print('登陆游戏')
        now_time = str(int(round(time.time() * 1000)))
        random.seed(hashlib.md5(self._username.encode('utf-8')).hexdigest())
        data_dict = {
            'client_version': self._version,
            'phone_type': 'huawei tag-al00',
            'phone_version': '5.1.1',
            'ratio': '1280*720',
            'service': 'CHINA MOBILE',
            'udid': str(random.randint(100000000000000, 999999999999999)),
            'source': 'android',
            'affiliate': 'WIFI',
            't': now_time,
            'e': self._build_url_tail(now_time),
            'gz': '1',
            'market': '2',
            'channel': self._channel,
            'version': self._version
        }
        random.seed()
        url_login_1 = f'{self._server}index/login/{uid}?&{urlencode(data_dict)}'
        self._requests.get(url=url_login_1)
        self._is_login = True

    def _build_url_tail(self, timestamp=str(int(round(time.time() * 1000)))):
        md5_raw = timestamp + 'ade2688f1904e9fb8d2efdb61b5e398a'
        md5 = hashlib.md5(md5_raw.encode('utf-8')).hexdigest()
        return f'&t={timestamp}&e={md5}&gz=1&market=2&channel={self._channel}&version={self._version}'

    @staticmethod
    def _encryption(url):
        times = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        data = f"POST\n{times}\n/{url.split('/', 3)[-1]}"
        mac = hmac.new(PASS_KEY.encode(), data.encode(), hashlib.sha1)
        data = mac.digest()
        return base64.b64encode(data).decode('utf-8'), times

    def _build_headers(self, url):
        data, times = self._encryption(url)
        return {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.4.1',
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': f'HMS {PASS_KEY_HEAD}:{data}',
            'Date': times
        }
