# from utils.stone import Stone
# from engine import Engine
from lobby import Lobby
from flask import Flask, request, jsonify
import numpy as np
import json

lobby = Lobby()

server = Flask(__name__)

@server.route("/hello")
def hello():
    return "Hello World!"

@server.route("/game-initialize", methods=['POST'])
def game_initialize():
    content = request.json
    if lobby.number_of_players == 0:
        lobby.add_new_player(content['nickName'])
        return jsonify({"status":0})
    elif lobby.number_of_players == 1:
        if lobby.p1_name == content['nickName']:
            return jsonify({"status":0})
        else:
            lobby.add_new_player(content['nickName'])
            if lobby.p1_name == content['nickName']:
                return jsonify({"status":1,"yourName":lobby.p1_name ,"oponentName": lobby.p2_name, "color":"black"})
            else:
                return jsonify({"status":1, "yourName":lobby.p2_name, "oponentName": lobby.p1_name, "color":"white"})
    else:
        if lobby.p1_name == content['nickName'] or lobby.p2_name == content['nickName']:
            if lobby.p1_name == content['nickName']:
                return jsonify({"status":1,"yourName":lobby.p1_name ,"oponentName": lobby.p2_name, "color":"black"})
            else:
                return jsonify({"status":1, "yourName":lobby.p2_name, "oponentName": lobby.p1_name, "color":"white"})
        else:
            return jsonify({"message":"Wystąpił błąd server jest pełen", "status":2})

@server.route("/move",  methods=['POST'])
def move():
    content = request.json
    lobby.engine.array = np.array(json.loads(content['array']))
    lobby.engine.move()
    r = json.dumps(lobby.engine.array.tolist())
    return jsonify({"status": "ok", "array" : r,  "whitePoints": lobby.engine.white_points, "blackPoints": lobby.engine.black_points})


@server.route("/status")
def status():
    return lobby.engine.return_status()


@server.route("/passing")
def passing():
    return lobby.engine.passing()

if __name__ == '__main__':
    server.run(debug=True)