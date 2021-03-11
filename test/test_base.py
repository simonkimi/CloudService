import base64
import datetime
import hashlib
import hmac

import requests

from game.constant import PASS_KEY, PASS_KEY_HEAD


def _encryption(url):
    times = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    data = f"POST\n{times}\n/{url.split('/', 3)[-1]}"
    mac = hmac.new(PASS_KEY.encode(), data.encode(), hashlib.sha1)
    data = mac.digest()
    return base64.b64encode(data).decode('utf-8'), times


def _build_headers(url):
    data, times = _encryption(url)
    return {
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.4.1',
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': f'HMS {PASS_KEY_HEAD}:{data}',
        'Date': times
    }


rsp = requests.post(url='https://passportapi.moefantasy.com/1.0/get/login/@self',
                    data='{"platform":"0","appid":"0","app_server_type":"0","password":"huanghuan789","username":"hyl7806331"}',
                    headers=_build_headers('https://passportapi.moefantasy.com/1.0/get/login/@self'))

print(rsp.text)
