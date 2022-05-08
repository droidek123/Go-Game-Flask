import requests
import sys

nick_name = sys.argv[1]
r = requests.post("http://127.0.0.1:5000/game-initialize", json={
    "nickName":nick_name
    })
if r.ok:
    print(r.json())
print(nick_name)