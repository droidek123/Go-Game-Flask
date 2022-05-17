"""Module implementing gui"""

from pickle import NONE
import sys
import math
import pygame
import numpy as np
import json

from utils.consts import (
    SIZE,
    MARGIN,
    BACKGROUND_COLORS,
    BLACK_STONE,
    WHITE_STONE,
    LEFT,
    RIGHT,
    BLACK_TXT,
    SCORE,
    MSG,
)
from utils.stone import Stone
from client import player_is_passing, check_status, move


class View:
    """Class implementing gui"""

    def __init__(self, name, oponent_name, color, id) -> None:
        """Constructor"""
        self.id = id 
        self.array = self.array = np.zeros((9, 9))
        self.list_of_points = self.calculate_grid_points(MARGIN, SIZE)
        self.black_points = 0
        self.white_points = 7.5
        self.is_game_ended = False
        self.color = color
        if self.color == 'white':
            self.stone = Stone.WHITE
        else:
            self.stone = Stone.BLACK
        self.font = None
        self.name = name
        self.oponent_name = oponent_name
        if color == 'black':
            self.is_blocked = False
        else:
            self.is_blocked = True
        self.end = False

    def init_pygame(self):
        "Game layout initialization"
        pygame.init()
        self.screen = pygame.display.set_mode((700, 700))
        self.font = pygame.font.SysFont("arial", 30)

    def draw(self):
        # Rysowanie tla i linii
        self.screen.fill(BACKGROUND_COLORS)
        for i in range(9):
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                self.list_of_points[0][i],
                self.list_of_points[1][i],
                4,
            )
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                self.list_of_points[2][i],
                self.list_of_points[3][i],
                4,
            )

        #Rysowanie kamieni
        for i in range(9):
            for j in range(9):
                if self.array[i][j] == Stone.BLACK:
                    pygame.draw.circle(
                        self.screen,
                        BLACK_STONE,
                        (self.list_of_points[2][i][1], self.list_of_points[0][j][0]),
                        20,
                    )
                elif self.array[i][j] == Stone.WHITE:
                    pygame.draw.circle(
                        self.screen,
                        WHITE_STONE,
                        (self.list_of_points[2][i][1], self.list_of_points[0][j][0]),
                        20,
                    )

         # Rysowanie punktacji          
        score = (
            f"{self.name}'s points: {self.black_points}"
            + f"     {self.oponent_name}'s points: {self.white_points}"
        )
        txt = self.font.render(score, True, BLACK_TXT)
        self.screen.blit(txt, SCORE)
        pygame.display.flip()


    def handle_game_finish(self):
        msg = NONE
        if self.black_points > self.white_points:
            msg = f"Wygrał Czarny"
        else:
            msg = f"Wygrał Biały"

        txt = self.font.render(msg, True, BLACK_TXT)
        self.screen.blit(txt, MSG)
        pygame.display.flip()

    def set_value_in_board(self, pos_x: int, pos_y: int, value: Stone) -> None:
        if self.array[pos_x][pos_y] == 0:
            self.array[pos_x][pos_y] = value
            return True
        else:
            return False

    def calculate_grid_points(self, margin, size, number_of_lines=9):
        # vertical points
        xp = np.linspace(margin, size - margin, number_of_lines)
        yp = np.full((number_of_lines), margin)
        svp = list(zip(xp, yp))

        yp = np.full((number_of_lines), size - margin)
        evp = list(zip(xp, yp))

        # horizontal points
        yp = np.linspace(margin, size - margin, number_of_lines)
        xp = np.full((number_of_lines), margin)
        shp = list(zip(xp, yp))

        xp = np.full((number_of_lines), size - margin)
        ehp = list(zip(xp, yp))

        return (svp, evp, shp, ehp)

    def update(self):
        events = pygame.event.get()
        if self.is_game_ended == True:
            self.handle_game_finish()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
        else:
            for event in events:
                if self.is_blocked == False and self.is_game_ended == False:
                    if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                        self.handle_click()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:
                        self.passing()
                if event.type == pygame.QUIT:
                    sys.exit()
            if self.is_blocked == True:
                response = check_status(self.id)
                if response['turn'] == self.color:
                    self.change_is_blocked()
                    self.white_points = response['whitePoints']
                    self.black_points = response['blackPoints']
                    self.is_game_ended = response['isGameEnded']
                    self.array = np.array(json.loads(response['array']))
                    self.draw()

    def handle_click(self):

        # get mouse cords
        pos_x, pos_y = pygame.mouse.get_pos()

        # calculate nearest row and column
        delta_x = math.inf
        delta_y = math.inf
        num_x = 0
        num_y = 0
        for i in range(9):
            temp_x = abs(self.list_of_points[2][i][1] - pos_x)
            temp_y = abs(self.list_of_points[0][i][0] - pos_y)
            if temp_x < delta_x:
                delta_x = temp_x
                num_x = i
            if temp_y < delta_y:
                delta_y = temp_y
                num_y = i
        is_click_valid = self.set_value_in_board(num_x, num_y, self.stone)
        if is_click_valid == False:
            return
        response = move(json.dumps(self.array.tolist()), self.id)
        self.array = np.array(json.loads(response['array']))
        self.white_points = response['whitePoints']
        self.black_points = response['blackPoints']
        self.change_is_blocked()

        # draw stone
        self.draw()

    def change_is_blocked(self):
        if self.is_blocked == False:
            self.is_blocked = True
        else:
            self.is_blocked = False

    def passing(self):
        response = player_is_passing(self.id)
        if response['correct'] == True:
            self.change_is_blocked()

        if response['isGameEnded'] == True:
            self.is_game_ended = response['isGameEnded']
            self.white_points = response['whitePoints']
            self.black_points = response['blackPoints']
        


