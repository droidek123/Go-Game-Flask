import requests
import json

def connect_to_lobby(nick_name):
    return requests.post("http://127.0.0.1:5000/game-initialize", json={
            "nickName":nick_name
            })

def player_is_passing():
    r = requests.get("http://127.0.0.1:5000/passing")
    return r.json()
    

def check_status():
    r = requests.get("http://127.0.0.1:5000/status")
    return r.json()

def move(array):
    r = requests.post("http://127.0.0.1:5000/move", 
        json={"array" : array}
    )
    return r.json()