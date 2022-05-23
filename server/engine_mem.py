""" Module implementing logic """

import sys
import numpy as np
import itertools
import networkx as nx
from flask import jsonify
import json

sys.path.append(".")
from utils.stone import Stone
from xmlrpc.client import boolean


class EngineMem:
    """Class implementing logic"""

    def find_groups(self, lobby):
        c = 0
        if lobby.turn == 'white':
            c = Stone.BLACK
        else:
            c = Stone.WHITE
        x, y = np.where(lobby.array == c)
        graph = nx.grid_graph(dim=[9, 9])
        stones = set(zip(x, y))
        all = set(itertools.product(range(9), range(9)))
        to_remove = all - stones
        graph.remove_nodes_from(to_remove)
        return nx.connected_components(graph)

    def find_liberties(self, group, lobby):
        for x, y in group:
            if x > 0 and lobby.array[x - 1, y] == 0:
                return False
            if y > 0 and lobby.array[x, y - 1] == 0:
                return False
            if x < lobby.array.shape[0] - 1 and lobby.array[x + 1, y] == 0:
                return False
            if y < lobby.array.shape[0] - 1 and lobby.array[x, y + 1] == 0:
                return False
        return True

    def return_status(self, lobby):
        return jsonify({"turn":lobby.turn, "isGameEnded": lobby.is_game_ended, "whitePoints": lobby.white_points, "blackPoints": lobby.black_points, "array" : json.dumps(lobby.array.tolist())})

    def passing(self, lobby):
        lobby.change_turn()
        lobby.pass_counter += 1
        if lobby.pass_counter == 2:
            lobby.is_game_ended = True
            return jsonify({"isGameEnded":lobby.is_game_ended, "correct": False, "whitePoints": lobby.white_points, "blackPoints": lobby.black_points})
        else:
            return jsonify({"isGameEnded":lobby.is_game_ended, "correct": True})

    def move(self, lobby):
        for group in list(self.find_groups(lobby)):
            if self.find_liberties(group, lobby):
                for i, j in group:
                    lobby.array[i][j] = Stone.EMPTY
                if lobby.turn == 'white':
                    lobby.white_points += len(group)
                else:
                    lobby.black_points += len(group)
        lobby.change_turn()

