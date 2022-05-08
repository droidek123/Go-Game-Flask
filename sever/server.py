from flask import Flask, request, jsonify
from lobby import Lobby

lobby = Lobby()

server = Flask(__name__)

@server.route("/hello")
def hello():
    return "Hello World!"

@server.route("/game-initialize", methods=['POST'])
def game_initialize():
    content = request.json
    print(content['nickName'])
    lobby.add_new_player(content['nickName'])
    if lobby.number_of_players == 1:
        return jsonify({"message":"Oczekiwanie na graczy"})
    elif lobby.number_of_players == 2:
        return jsonify({"message":"Dwóch graczy rozpoczynamy rozgrywkę"})
    else:
        return jsonify({"message":"Wystąpił błąd"})

if __name__ == '__main__':
    server.run(debug=True)