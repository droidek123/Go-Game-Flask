import numpy as np

class Lobby:

    def __init__(self, id):
        self.id = id
        self.number_of_players = 0
        self.p1_name = None
        self.p2_name = None
        self.is_full = False
        self.white_points = 7.5
        self.black_points = 0
        self.pass_counter = 0
        self.is_game_ended = False
        self.turn =  "black"
        self.url = "C:\\Users\\Andrzej\\Desktop\\Studia\\Sem6\\DPP\\iolszewski252737_go_flask\\server\\db\\lobby" + str(self.id) + ".txt"
        self.create_file()

    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
    
    def create_file(self):
        file = open(self.url, "w")
        for row in np.zeros((9,9)):
            np.savetxt(file, row)
        file.close()

    def get_array(self):
        return np.loadtxt(self.url).reshape(9, 9)

    def add_new_player(self, name):
        self.number_of_players += 1
        if self.number_of_players == 1:
            self.p1_name = name
        else:
            self.p2_name = name
            self.is_full = True
