import requests
import zlib

url = 'http://login.jr.moefantasy.com/index/hmLogin/9a92f07a6f337787bdf3e0f3945a4b57&t=1615472895875&e=954337e21bb893b4fb3023425349bac9&gz=1&market=2&channel=100011&version=5.2.0'

headers = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; 16th Build/OPM1.171019.026)'
}

rsp = requests.post(url=url, headers=headers)


print(zlib.decompress(rsp.content).decode())
print(rsp.headers)

