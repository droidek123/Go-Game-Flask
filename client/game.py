import requests
import time
import sys
import json
import pygame
from view import View 
from client import connect_to_lobby, check_status

def main():
    nick_name = sys.argv[1]
    status = 0
    while status == 0:
        r = connect_to_lobby(nick_name)
        if r.ok:
            reponse = r.json()
            if reponse['status'] == 0:
                print("Oczekiwanie na przeciwnika...")
                time.sleep(5.0)
            elif reponse['status'] == 1:
                status = 1
                yourName = reponse['yourName']
                oponentName = reponse['oponentName']
                color = reponse['color']

        else:
            print("Nie można polaczyc sie z serverem")
            return


    if color == "black":
        view = View(yourName, oponentName, color)
    else:
          view = View(oponentName, yourName, color)
    view.init_pygame()
    view.draw()
    while True:
        view.update()
        pygame.time.wait(100)


if __name__ == '__main__':
    main()
