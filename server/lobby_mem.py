import numpy as np

class LobbyMem:

    def __init__(self, id):
        self.id = id
        self.number_of_players = 0
        self.p1_name = None
        self.p2_name = None
        self.is_full = False
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

    def add_new_player(self, name):
        self.number_of_players += 1
        if self.number_of_players == 1:
            self.p1_name = name
        else:
            self.p2_name = name
            self.is_full = True
