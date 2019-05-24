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
from random import randrange


class Labyrinth:

    """ This class manage all the non-player functions as generating the maze design and the items positions """

    def __init__(self, window):
        wall = pygame.image.load("images/wall.png").convert_alpha()
        start = pygame.image.load("images/start.png").convert_alpha()
        ground = pygame.image.load("images/ground.png").convert_alpha()
        """The 'free_sprite' list will contain all the tuples surfaces of the sprites on which the items to collect 
        may blit. Not on the walls, the player, the keeper and a few positions too close to him."""
        self.free_sprites = []
        self.window = window


        """ This function read the datas in the 'structure.py' file and assign to each number an image (wall, ground 
          or start), and a surface position. """

        num_ligne = 0
        for ligne in open("structure.py"):
            num_case = 0
            for sprite in ligne:
                x = num_case * sprite_size
                y = num_ligne * sprite_size
                if sprite in ("0", "3"):
                    position = (x, y)
                    window.blit(ground, position)
                    """All the free sprites tuples surfaces will be added to the list during this process."""
                    if sprite == "0":
                        self.free_sprites.append(position)
                elif sprite == '1':
                    window.blit(wall, (x, y))
                elif sprite == '2':
                    window.blit(start, (x, y))
                num_case += 1
            num_ligne += 1

    """This function will permit to place the three items to collect randomly in the maze 
    each tim the game will be open"""
    def initialize_items(self):
        self.needle = pygame.image.load("images/needle.png").convert_alpha()
        self.ether = pygame.image.load("images/ether.png").convert_alpha()
        self.tube = pygame.image.load("images/plastic_tube.png").convert_alpha()

        for item in (self.tube, self.ether, self.needle):
            """Each item takes a random position in the free_sprite list."""
            position_idx = randrange(0, len(self.free_sprites) - 1)
            """The position took by an item is removed from the list. 
            That will avoid the next item to takes the same position.
            We can use '.pop' or 'remove'"""
            xy = self.free_sprites.pop(position_idx)
            # self.free_sprites.remove(xy)
            self.window.blit(item, xy)
            self.item_references = {
                xy: item
            }

class Player:

    """This class manage all the player attributes and functions."""

    @property
    def position(self):
        return self.x, self.y,

    def __init__(self, icone, window):
        self.icone = pygame.image.load("images/MacGyver.png").convert_alpha()
        self.case_x = 0
        self.case_y = 0
        self.x = 0
        self.y = 0

class Keeper(Player):

    """This descendant class only manage the keeper position in the maze. He may have be handled in the
    Labyrinth class. However this option could permit to work on a game enhancement or an add-on.
    The keeper may get an aggressive behaviour. Or for a multi-player project."""

    def __init__(self, icone, window):
        self.icone = pygame.image.load("images/keeper.png").convert_alpha()
        self.x = 700
        self.y = 700

def main():

    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption("FREE MACGYVER")

    maze = Labyrinth(window)
    maze.initialize_items()
    macgyver = Player("images/MacGyver.png", window)
    keeper = Keeper("images/keeper.png", window)

    """ Main loop containing the game code. It allows to run the game as long as the player doesn't quit. """
    continuer = 1
    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0


        window.blit(macgyver.icone, macgyver.position)
        window.blit(keeper.icone, keeper.position)

        pygame.display.flip()


if __name__ == '__main__':
    main()
