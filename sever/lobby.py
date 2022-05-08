class Lobby:

    def __init__(self):
        self.number_of_players = 0
        self.p1_name = None
        self.p2_name = None

    def add_new_player(self, name):
        self.number_of_players += 1
        if self.number_of_players == 1:
            self.p1_name = name
        else:
            self.p2_name = name
        
