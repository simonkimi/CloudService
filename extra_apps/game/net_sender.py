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
from extra_apps.game.constant import URL_IOS_VERSION, URL_VERSION, PASS_KEY, PASS_KEY_HEAD


class NetSender:
    def __init__(self):
        self._cookies = None
        self._version = None
        self._channel = None

    def login(self, username: str, password: str, server: int):
        url_version = URL_VERSION if server <= 3 else URL_IOS_VERSION
        self._channel = '100011' if server <= 3 else '100015'
        # 获取版本信息
        try:
            rep = requests.get(url=url_version).json()
            if 'version' not in rep:
                raise Exception('version不在登陆中, 服务器正在维护')

            self._version = rep['version']['newVersionId']
            login_server = rep['loginServer']
            hm_login_server = rep['hmLoginServer']
        except Exception as e:
            Log.e('NetSender.login.version', '获取Version出错', f'用户名:{username}', str(e))
            raise Exception('NetSender.login.version ' + str(e))

        # 获取token
        try:
            url_token = f'{hm_login_server}1.0/get/login/@self'
            login_data = json.dumps({
                "platform": "0",
                "appid": "0",
                "app_server_type": "0",
                "password": password,
                "username": username
            }).replace(" ", "")
            rsp = requests.post(url=url_token, data=login_data, headers=self._build_headers(url_token)).json()
            if "error" in rsp and int(rsp["error"]) != 0:
                raise Exception(f'code:{rsp["error"]} msg:{rsp["errmsg"]}')
            token = rsp['access_token']
        except Exception as e:
            Log.e('NetSender.login.token', '获取Token出错', f'用户名:{username}', str(e))
            raise Exception('NetSender.login.token ' + str(e))

        # 验证token并获取游戏token
        try:
            url_info = f'{hm_login_server}1.0/get/userInfo/@self'
            data = json.dumps({"access_token": token})
            rsp = requests.post(url=url_token, data=data, headers=self._build_headers(url_info)).json()
            if "error" in rsp and int(rsp["error"]) != 0:
                raise Exception(f'验证Token出错:{rsp["errmsg"]}')
        except Exception as e:
            Log.e('NetSender.login.url_info)', '验证Token出错', f'用户名:{username}', str(e))
            raise Exception('NetSender.login.url_info ' + str(e))

        # 获取用户Cookies
        try:
            url_login = f'{login_server}index/hmLogin/{token}{self._build_url_tail()}'
            rsp = requests.get(url=url_login)
            self._cookies = rsp.cookies.get_dict()
            rsp_data = json.loads(zlib.decompress(rsp.content))
            uid = rsp_data['userId']
        except Exception as e:
            Log.e('NetSender.login.url_login)', '获取Token出错', f'用户名:{username}', str(e))
            raise Exception('NetSender.login.url_login ' + str(e))

        # 正式登录游戏
        now_time = str(int(round(time.time() * 1000)))
        random.seed(hashlib.md5(username.encode('utf-8')).hexdigest())
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
        url_login_1 = f'{login_server}index/login/{uid}?&{urlencode(data_dict)}'
        requests.get(url=url_login_1)

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


if __name__ == '__main__':
    sender = NetSender()
    sender.login('simon_xu', 'xusong404', 0)
