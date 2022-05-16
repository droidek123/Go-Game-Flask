from engine import Engine


class Lobby:

    def __init__(self):
        self.id = 0
        self.number_of_players = 0
        self.p1_name = None
        self.p2_name = None
        self.engine = Engine(self.id)
        self.is_full = False

    def add_new_player(self, name):
        self.number_of_players += 1
        if self.number_of_players == 1:
            self.p1_name = name
        else:
            self.p2_name = name
            self.is_full = True
