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

    def __init__(self, id):
        """Constructor"""
        self.array = np.zeros((9, 9))
        self.white_points = 7.5
        self.black_points = 0
        self.pass_counter = 0
        self.is_game_ended = False
        self.turn =  "black"

    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"


    def set_value_in_board(self, pos_x: int, pos_y: int, value: Stone) -> None:
        self.array[pos_x][pos_y] = value

    def is_place_free(self, pos_x: int, pos_y: int) -> boolean:
        return True if self.array[pos_x][pos_y] == 0 else False

    def find_groups(self, color):
        c = 0
        if color == 'white':
            c = Stone.BLACK
        else:
            c = Stone.WHITE
        x, y = np.where(self.array == c)
        graph = nx.grid_graph(dim=[9, 9])
        stones = set(zip(x, y))
        all = set(itertools.product(range(9), range(9)))
        to_remove = all - stones
        graph.remove_nodes_from(to_remove)
        return nx.connected_components(graph)

    def find_liberties(self, group):
        for x, y in group:
            if x > 0 and self.array[x - 1, y] == 0:
                return False
            if y > 0 and self.array[x, y - 1] == 0:
                return False
            if x < self.array.shape[0] - 1 and self.array[x + 1, y] == 0:
                return False
            if y < self.array.shape[0] - 1 and self.array[x, y + 1] == 0:
                return False
        return True

    def return_status(self):
        return jsonify({"turn": self.turn, "isGameEnded":self.is_game_ended, "whitePoints": self.white_points, "blackPoints": self.black_points, "array" : json.dumps(self.array.tolist())})

    def passing(self):
        self.change_turn()
        self.pass_counter += 1
        if self.pass_counter == 2:
            self.is_game_ended = True
            return jsonify({"isGameEnded":self.is_game_ended, "correct": False, "whitePoints": self.white_points, "blackPoints": self.black_points})
        else:
            return jsonify({"isGameEnded":self.is_game_ended, "correct": True})

    def move(self):
        for group in list(self.find_groups(self.turn)):
            if self.find_liberties(group):
                for i, j in group:
                    self.array[i][j] = Stone.EMPTY
                if self.turn == 'white':
                    self.white_points += len(group)
                else:
                    self.black_points += len(group)
        self.change_turn()
