# from utils.stone import Stone
from engine import Engine
from lobby import Lobby
from engine_mem import EngineMem
from lobby_mem import LobbyMem
from flask import Flask, request, jsonify
import numpy as np
import json
import sys

counter = 0
engine = None
lobbys = list()
mode = None

server = Flask(__name__)

@server.route("/hello")
def hello():
    return "Hello World!"

@server.route("/game-initialize", methods=['POST'])
def game_initialize():
    global counter
    global engine


    if not lobbys:
        if mode == 'file':
            engine = Engine()
            lobbys.append(Lobby(counter))
            counter += 1
        if mode == 'mem':
            engine = EngineMem()
            lobbys.append(LobbyMem(counter))
            counter += 1
    content = request.json

    # oczekiwanie na gracza
    if content['id'] != -1:
        if lobbys[content['id']].number_of_players == 1: # gdy w pokoju jest jeden gracz
            return jsonify({"id" : lobbys[content['id']].id, "status":0})
        elif lobbys[content['id']].number_of_players == 2:
            if lobbys[content['id']].p1_name == content['nickName']:
                return jsonify({"id" : lobbys[content['id']].id, "status":1,"yourName":lobbys[content['id']].p1_name ,"oponentName": lobbys[content['id']].p2_name, "color":"black"})
            else:
                return jsonify({"id" : lobbys[content['id']].id, "status":1, "yourName":lobbys[content['id']].p2_name, "oponentName": lobbys[content['id']].p1_name, "color":"white"})
    else:
        if lobbys[len(lobbys)-1].number_of_players == 0:
            lobbys[len(lobbys)-1].add_new_player(content['nickName'])
            return jsonify({"status":0, "id" : lobbys[len(lobbys)-1].id})
        elif lobbys[len(lobbys)-1].number_of_players == 1:
            lobbys[len(lobbys)-1].add_new_player(content['nickName'])
            if mode == 'file':
                lobbys.append(Lobby(counter))
            else:
                lobbys.append(LobbyMem(counter))
            counter += 1
            if lobbys[len(lobbys)-1].p1_name == content['nickName']:
                return jsonify({"id" : lobbys[len(lobbys)-2].id, "status":1,"yourName":lobbys[len(lobbys)-2].p1_name ,"oponentName": lobbys[len(lobbys)-2].p2_name, "color":"black"})
            else:
                return jsonify({"id" : lobbys[len(lobbys)-2].id, "status":1, "yourName":lobbys[len(lobbys)-2].p2_name, "oponentName": lobbys[len(lobbys)-2].p1_name, "color":"white"})
 
@server.route("/move",  methods=['POST'])
def move():
    global engine
    content = request.json
    array = np.array(json.loads(content['array']))
    if mode == "file":
        array = engine.move(lobbys[content['id']], array)
        file = open(lobbys[content['id']].url, "w")
        for row in array:
            np.savetxt(file, row)
        file.close()
        r = json.dumps(array.tolist())
    else:
        lobbys[content['id']].array = array
        engine.move(lobbys[content['id']])
        r = json.dumps(lobbys[content['id']].array.tolist())
    return jsonify({"status": "ok", "array" : r,  "whitePoints": lobbys[content['id']].white_points, "blackPoints": lobbys[content['id']].black_points})


@server.route("/status")
def status():
    global engine
    content = request.json
    return engine.return_status(lobbys[content['id']])


@server.route("/passing")
def passing():
    global engine
    content = request.json
    return engine.passing(lobbys[content['id']])

if __name__ == '__main__':
    mode = sys.argv[1]
    server.run(debug=True)