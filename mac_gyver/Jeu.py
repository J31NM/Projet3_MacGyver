#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
FREE MACGYVER

Little game in witch the player embodies Macgyver who needs to escape from a maze after having incapacitated his keeper.
In order to put him away, Macgyver has to sedate him with a tranquilizer into a syringe.
Besides his unlimited engineering skills, Macgyver will needs three items randomly arranged in the maze to build the syringe:
a needle, a bottle of ether and a plastic tube.
The player fail if he finds the exit without the syringe.
Only Macgyver can move, the keeper is immobile next to the exit.

Script Python
Files : jeu.py, requirements.py, structure.py, constants.py + images
"""

import pygame
from pygame.locals import *

from constants import *

pygame.init()

window = pygame.display.set_mode((window_side, window_side))

pygame.display.set_caption("FREE MACGYVER")

class Labyrinth:

    """ This class manage all the non-player functions as generating the maze design and the items management """

    def __init__(self):
        wall = pygame.image.load("images/mur.png").convert_alpha()
        start = pygame.image.load("images/depart.png").convert_alpha()
        ground = pygame.image.load("images/sol.png").convert_alpha()

        """ This function read the datas in the 'structure.py' file and assign to each number an image (wall, ground 
          or start), and a surface position. """

        num_line = 0
        for line in open("structure.py"):
            num_case = 0
            for sprite in line:
                x = num_case * sprite_size
                y = num_line * sprite_size
                if sprite == '1':
                    window.blit(wall, (x, y))
                elif sprite == '2':
                    window.blit(start, (x, y))
                elif sprite == '0' or '3':
                    window.blit(ground, (x, y))
                num_case += 1
            num_line += 1


""" Main loop containing the game code. It allows to run the game as long as the player doesn't quit. """

continuer = 1
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0

        """ this line calls the labyrinth class which generates the maze. """
        labyrinth = Labyrinth()

        pygame.display.flip()