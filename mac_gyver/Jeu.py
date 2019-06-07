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


class ItemBase(object):
    """
    This class will allow to manage the all the items in the game.
    """

    @property
    def position(self):
        return self.x, self.y,

    @position.setter
    def position(self, position):
        self.x, self.y = position

    def __init__(self, icon, position):
        self.icon = pygame.image.load(icon).convert_alpha()
        self.x, self.y = position

    def display(self):
        pass

class Item(ItemBase):
    """
    Needle, plastic tube and ether
    """

class Maze:

    """ This class manage all the non-player functions as generating the maze design and the items positions """

    def __init__(self, window):
        self.window = window

        """We need to open the file 'structure.py' to build the maze, and close it after having read it in order to 
        avoid keep it opened."""
        with open("structure.py") as fd:
            self.structure = fd.readlines()

        """The 'free_sprite' list will contain all the tuples surfaces of the sprites on which the items to collect 
        may blit. Not on the walls, the player, the keeper and a few positions too close to him."""
        self.free_sprites = []

        self.needle = None
        self.ether = None
        self.tube = None
        self.syringe = None
        self.ground = None

        self.initialize()

    def initialize(self):
        self.display_structure()
        self.initialize_items()
        self.display_items()


    def display_items(self):
        for item in (self.tube, self.ether, self.needle):
            self.window.blit(item.icon, item.position)

    """ This function read the datas in the 'structure.py' file and assign to each number an image (wall, ground 
        or start), and a surface position. """
    def display_structure(self):
        wall = pygame.image.load("images/wall.png").convert_alpha()
        start = pygame.image.load("images/start.png").convert_alpha()
        ground = pygame.image.load("images/ground.png").convert_alpha()

        line_num = 0
        for ligne in self.structure:
            case_num = 0
            for sprite in ligne.strip():
                x = case_num * sprite_size
                y = line_num * sprite_size
                if sprite in ("0", "3"):
                    position = (x, y)
                    self.window.blit(ground, position)
                    """All the free sprites tuples surfaces will be added to the list during this process."""
                    if sprite == "0":
                        self.free_sprites.append(position)
                elif sprite == '1':
                    self.window.blit(wall, (x, y))
                elif sprite == '2':
                    self.window.blit(start, (x, y))
                case_num += 1
            line_num += 1

    """ This function assign a random position to each three items into the maze and takes care they will not pick up
        the same adress twice."""
    def initialize_items(self):
        self.item_references = {}

        position_idx = randrange(0, len(self.free_sprites) - 1)
        xy = self.free_sprites.pop(position_idx)
        self.tube = Item("images/plastic_tube.png", xy)
        self.item_references[xy] = self.tube

        position_idx = randrange(0, len(self.free_sprites) - 1)
        xy = self.free_sprites.pop(position_idx)
        self.ether = Item("images/ether.png", xy)
        self.item_references[xy] = self.ether

        position_idx = randrange(0, len(self.free_sprites) - 1)
        xy = self.free_sprites.pop(position_idx)
        self.needle = Item("images/needle.png", xy)
        self.item_references[xy] = self.needle

class Player:
    """This class manage all the player attributes and functions. His position and the movements."""

    """We assign a position to the player. 'x' for the easting and 'y' for the northing.
    That will allow to control his position on the maze checkerboard and to interact with the items."""
    @property
    def position(self):
        return self.x, self.y,

    def __init__(self, icon, initial_position=None):
        """Be sure that the player will begin the game at the top left position."""
        initial_position = initial_position or (0, 0)
        self.icon = pygame.image.load(icon).convert_alpha()
        """The cases correspond to the structure. 
        Each move from the player will also be located in in the 'structure.py board."""
        self.case_x = 0
        self.case_y = 0
        self.x, self.y = initial_position

        """Read the structure to interact with the differnts sprites types."""
        with open("structure.py") as fd:
            self.structure = fd.readlines()

    def move(self, direction):
        if direction == K_RIGHT:
            """Check if we are against the window frame before to allow the move."""
            if self.x < (window_width - 50):
                """Check if the next sprite is a wall or a ground before to allow the move."""
                if self.structure[self.case_y][self.case_x + 1] != '1':
                    """Update the position in the structure grid."""
                    self.case_x += 1
        elif direction == K_LEFT:
            if self.x > 0:
                if self.structure[self.case_y][self.case_x - 1] != '1':
                    self.case_x -= 1
        elif direction == K_UP:
            if self.y > 0:
                if self.structure[self.case_y - 1][self.case_x] != '1':
                    self.case_y -= 1
        elif direction == K_DOWN:
            """In this case we need to avoid to move the player in the inventory line. So -100 instead of -50 pixels"""
            if self.y < (window_height - 100):
                if self.structure[self.case_y + 1][self.case_x] != '1':
                    self.case_y += 1
        else:
            raise ValueError('Unknown Direction')

        self.x = self.case_x * sprite_size
        self.y = self.case_y * sprite_size

class Keeper(Player):

    """This descendant class only manage the keeper position in the maze. He may have be handled in the
    Labyrinth class. However this option could permit to work on a game enhancement or an add-on.
    The keeper may get an aggressive behaviour. Or for a multi-player project."""

def main():
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption("FREE MACGYVER")

    maze = Maze(window)
    macgyver = Player("images/MacGyver.png")
    keeper = Keeper("images/keeper.png", initial_position=(700, 700))

    """ Main loop containing the game code. It allows to run the game as long as the player doesn't quit. """
    continuer = 1
    while continuer:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0

            if event.type == KEYDOWN:
                macgyver.move(event.key)

            maze.display_structure()
            maze.display_items()

            window.blit(macgyver.icon, macgyver.position)
            window.blit(keeper.icon, keeper.position)

            pygame.display.flip()

if __name__ == '__main__':
    main()
