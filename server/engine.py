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


class Engine:
    """Class implementing logic"""

    # def set_value_in_board(self, pos_x: int, pos_y: int, value: Stone) -> None:
    #     self.array[pos_x][pos_y] = value

    # def is_place_free(self, pos_x: int, pos_y: int) -> boolean:
    #     return True if self.array[pos_x][pos_y] == 0 else False

    def find_groups(self, lobby, array):
        c = 0
        if lobby.turn == 'white':
            c = Stone.BLACK
        else:
            c = Stone.WHITE
        x, y = np.where(array == c)
        graph = nx.grid_graph(dim=[9, 9])
        stones = set(zip(x, y))
        all = set(itertools.product(range(9), range(9)))
        to_remove = all - stones
        graph.remove_nodes_from(to_remove)
        return nx.connected_components(graph)

    def find_liberties(self, group, array):
        for x, y in group:
            if x > 0 and array[x - 1, y] == 0:
                return False
            if y > 0 and array[x, y - 1] == 0:
                return False
            if x < array.shape[0] - 1 and array[x + 1, y] == 0:
                return False
            if y < array.shape[0] - 1 and array[x, y + 1] == 0:
                return False
        return True

    def return_status(self, lobby):
        return jsonify({"turn":lobby.turn, "isGameEnded": lobby.is_game_ended, "whitePoints": lobby.white_points, "blackPoints": lobby.black_points, "array" : json.dumps(lobby.get_array().tolist())})

    def passing(self, lobby):
        lobby.change_turn()
        lobby.pass_counter += 1
        if lobby.pass_counter == 2:
            lobby.is_game_ended = True
            return jsonify({"isGameEnded":lobby.is_game_ended, "correct": False, "whitePoints": lobby.white_points, "blackPoints": lobby.black_points})
        else:
            return jsonify({"isGameEnded":lobby.is_game_ended, "correct": True})

    def move(self, lobby, array):
        for group in list(self.find_groups(lobby, array)):
            if self.find_liberties(group, array):
                for i, j in group:
                    array[i][j] = Stone.EMPTY
                if lobby.turn == 'white':
                    lobby.white_points += len(group)
                else:
                    lobby.black_points += len(group)
        lobby.change_turn()
        return array
