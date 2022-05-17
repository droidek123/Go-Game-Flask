import requests
import json

def connect_to_lobby(nick_name, id):
    return requests.post("http://127.0.0.1:5000/game-initialize", json={
            "nickName":nick_name, "id" : id
            })

def player_is_passing(id):
    r = requests.get("http://127.0.0.1:5000/passing", json={
            "id" : id
            })
    return r.json()
    

def check_status(id):
    r = requests.get("http://127.0.0.1:5000/status", json={
            "id" : id
            })
    return r.json()

def move(array, id):
    r = requests.post("http://127.0.0.1:5000/move", json={
        "array" : array, "id" : id
        })
    return r.json()