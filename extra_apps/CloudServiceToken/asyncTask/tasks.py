import json
import requests
import base64
import datetime
import hmac
import hashlib
from .app import app

PASS_KEY = "kHPmWZ4zQBYP24ubmJ5wA4oz0d8EgIFe"
PASS_KEY_HEAD = "881d3SlFucX5R5hE"


@app.task()
def get_token(username: str, password: str, server: int) -> {}:
    print(username, password, server)
    session = requests.session()
    login_url = 'https://passportapi.moefantasy.com/' if server <= 3 else 'https://iospassportapi.moefantasy.com/'
    url_token = f'{login_url}1.0/get/login/@self'
    login_data = json.dumps({
        "platform": "0",
        "appid": "0",
        "app_server_type": "0",
        "password": password,
        "username": username
    }).replace(" ", "")

    try:
        rsp = session.post(url=url_token, data=login_data, headers=build_headers(url_token))
        if 'nginx' in rsp.text:
            return {
                'error': '400',
                'errmsg': '服务器被风控, nginx'
            }
        rsp_json = rsp.json()

        if "error" in rsp_json and int(rsp_json["error"]) != 0:
            if int(rsp_json['error']) == 21003:
                return {
                    'error': '401',
                    'errmsg': '用户名或密码错误'
                }
            return {
                'error': '404',
                'errmsg': f'code:{rsp_json["error"]} msg:{rsp_json["errmsg"] if "errmsg" in rsp else ""}'
            }
        token = rsp_json['access_token']
        return {
            'token': token,
        }
    except Exception as e:
        return {
            'error': '500',
            'errmsg': str(e)
        }


def encryption(url):
    times = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    data = f"POST\n{times}\n/{url.split('/', 3)[-1]}"
    mac = hmac.new(PASS_KEY.encode(), data.encode(), hashlib.sha1)
    data = mac.digest()
    return base64.b64encode(data).decode('utf-8'), times


def build_headers(url):
    data, times = encryption(url)
    return {
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.4.1',
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': f'HMS {PASS_KEY_HEAD}:{data}',
        'Date': times
    }
