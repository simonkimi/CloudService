import requests

rsp = requests.post(
    url='http://127.0.0.1:8000/user/setting/',
    json={
        'pvp_fleet': 5,
        'pvp_format': 4,
        'pvp_night': True
    },
    headers={
        'authorization': 'Token 761b0fc88bf1c5ba342c7a8d3e3bd5a33d64aaa5'
    }
)

print(rsp.json())
