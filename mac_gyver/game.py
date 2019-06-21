#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
FREE MACGYVER

Little game in witch the player embodies Macgyver who needs to escape from a maze
after having incapacitated his keeper.
In order to put him away, Macgyver has to sedate him with a tranquilizer into a syringe.
Besides his unlimited engineering skills, Macgyver will needs three items
randomly arranged in the maze to build the syringe: a needle, a bottle of ether and a plastic tube.
The player fail if he finds the exit without the syringe.
Only Macgyver can move, the keeper is immobile next to the exit.

Script Python
Files : game.py, structure.py, constants.py + images

"""

from random import randrange
import pygame
from pygame import locals as pygame_locals
from constants import *

# pylint: disable=E1101
# Module 'pygame.locals' has no 'K_RIGHT' member (no-member)

# pylint: disable=W0614
# Unused import BLACK from wildcard import (unused-wildcard-import)



class ItemBase:
    """This class will allow to manage all the items in the game."""

    @property
    def position(self):
        """Position needed for the interactions with the player"""
        return self.x, self.y

    @position.setter
    def position(self, position):
        self.x, self.y = position

    def __init__(self, icon, position):
        self.icon = pygame.image.load(icon).convert_alpha()
        # pylint: disable=C0103
        self.x, self.y = position


class Maze:
    """ This class manage all the non-player functions as generating the maze design
        and the items positions """

    def __init__(self, window):
        self.window = window

        # We need to open the file 'structure.py' to build the maze,
        # and close it after having read it in order to avoid keep it opened.
        with open("structure.py") as stru:
            self.structure = stru.readlines()

        # The 'free_sprite' list will contain all the tuples surfaces of the sprites on which
        # the items to collect may blit. Not on the walls, the player,
        # the keeper and a few positions too close to him.
        self.free_sprites = []

        # The 'inventory' list will contain the items picked up by the player.
        # This list will be used later to define if the player win or loose
        # when he will meet the keeper.
        # If the list is full and contain three items he wins, otherwise he looses.
        self.inventory = []

        # The 'item_references' dictionary will contain the surfaces of each items.
        # We will use it to blit the right item in the inventory window.
        self.item_references = {}

        # The 'inventory_position' list of tuples contain the three sprites surfaces where
        # the items can blit after have been collected by the player, at the bottom of the window.
        self.inventory_position = [(50, 750), (100, 750), (150, 750)]

        self.counter = 0

        self.sentence = ""

        self.needle = None
        self.ether = None
        self.tube = None
        self.equal = None
        self.syringe = None
        self.ground = None

        self.initialize()

    def initialize(self):
        """Automatically launch those four functions when the Class Maze is called in main."""
        self.initialize_textures()
        self.display_structure()
        self.initialize_items()
        self.display_items()

    def initialize_textures(self):
        """Three images who appear during the game."""
        self.equal = pygame.image.load("images/equal.png").convert_alpha()
        self.syringe = pygame.image.load("images/syringe.png").convert_alpha()
        self.ground = pygame.image.load("images/ground.png").convert_alpha()

    def display_structure(self):
        """ This function read the data in the 'structure.py' file and assign to each number
        an image(wall, ground or start), and a surface position."""

        wall = pygame.image.load("images/wall.png").convert_alpha()
        start = pygame.image.load("images/start.png").convert_alpha()
        ground = pygame.image.load("images/ground.png").convert_alpha()
        backpack = pygame.image.load("images/backpack.png").convert_alpha()
        inventory = pygame.image.load("images/inventory.png").convert_alpha()
        penny = pygame.image.load("images/penny.png").convert_alpha()

        line_num = 0
        for line in self.structure:
            case_num = 0
            for sprite in line.strip():
                # pylint: disable=C0103
                x = case_num * sprite_size
                # pylint: disable=C0103
                y = line_num * sprite_size
                if sprite in ("0", "3"):
                    position = (x, y)
                    self.window.blit(ground, position)
                    # All the free sprites tuples surfaces will be added to the list.
                    if sprite == "0":
                        self.free_sprites.append(position)
                elif sprite == '1':
                    self.window.blit(wall, (x, y))
                elif sprite == '2':
                    self.window.blit(start, (x, y))
                elif sprite == 'b':
                    self.window.blit(backpack, (x, y))
                elif sprite == '4':
                    self.window.blit(inventory, (x, y))
                elif sprite == 'p':
                    self.window.blit(penny, (x, y))
                case_num += 1
            line_num += 1

    def initialize_items(self):
        """ This function assign a random position to each three items into the maze
                and takes care they will not pick up the same address twice."""

        self.item_references = {}

        position_idx = randrange(0, len(self.free_sprites) - 1)
        coord = self.free_sprites.pop(position_idx)
        self.tube = ItemBase("images/plastic_tube.png", coord)
        self.item_references[coord] = self.tube

        position_idx = randrange(0, len(self.free_sprites) - 1)
        coord = self.free_sprites.pop(position_idx)
        self.ether = ItemBase("images/ether.png", coord)
        self.item_references[coord] = self.ether

        position_idx = randrange(0, len(self.free_sprites) - 1)
        coord = self.free_sprites.pop(position_idx)
        self.needle = ItemBase("images/needle.png", coord)
        self.item_references[coord] = self.needle

    def display_items(self):
        """Blit each of the three items at the position they randomly took
            in the free_sprite list."""
        for item in (self.tube, self.ether, self.needle):
            self.window.blit(item.icon, item.position)

    def manage_inventory(self, coord):
        """The 'manage_inventory' function manage the behaviour of each item when the player collect
            them. A ground image appear in order to hide the item collected.
            The item appear in the inventory.
            If the three items are collected, an 'equal' sign and the syringe appear.
            Equal symbolize the assembly."""
        self.counter = 0
        item = self.item_references.pop(coord)
        self.window.blit(self.ground, coord)
        try:
            item.position = self.inventory_position.pop(self.counter)
            self.window.blit(item.icon, item.position)
            if len(self.inventory) == 3:
                self.window.blit(self.equal, (200, 750))
                self.window.blit(self.syringe, (250, 750))
        except IndexError:
            pass
        self.counter += 1

    def is_sprite_item(self, coord):
        """Return the position of each of the three items """
        return coord in self.item_references

    # This property will be used to choose the right message for the player
    # depending of how many items he has.
    @property
    def items_count(self):
        """Return the length of Macgyver's inventory"""
        return len(self.inventory)


    def choose_text(self, coord):
        """ This function will manage the messages for the player, indications,
                advices and victory or game over texts.
                I choose to add the character of Penny who is Macgyver friend.
                The messages will appear in the inventory line at the bottom of the window.
            """
        myfont = pygame.font.SysFont('Comic Sans MS', 14)
        items_count = self.items_count
        # They are two options for the messages.
        # In the first one the player is in the maze and continue to play.
        # If the player go on the keeper sprite, he activate the final message, victory or fail.
        if coord != (700, 700,):
            if items_count == 0:
                self.sentence = 'Intro'
            elif items_count == 1:
                self.sentence = 'first_item'
            elif items_count == 2:
                self.sentence = 'second_item'
            elif items_count == 3:
                self.sentence = 'syringe'
        else:
            if items_count == 3:
                self.sentence = 'victory'
            else:
                self.sentence = 'fail'
        line_space = 20
        # pylint: disable=C0103
        x, y = (360, 750,)
        for line in MESSAGES[self.sentence]:
            line_surface = myfont.render(line, False, WHITE)
            self.window.blit(line_surface, (x, y))
            y += line_space


class Player:
    """This class manage all the player attributes and functions.
        His position and the movements."""

    # We assign a position to the player. 'x' for the easting and 'y' for the northing.
    # That will allow to control his position on the maze checkerboard
    # and to interact with the items.
    @property
    def position(self):
        """Position needed for the interactions in the game"""
        return self.x, self.y

    def __init__(self, icon, initial_position=None):
        # Be sure that the player will begin the game at the top left position.
        initial_position = initial_position or (0, 0)
        self.icon = pygame.image.load(icon).convert_alpha()
        # The cases correspond to the structure.
        # Each move from the player will also be located in in the 'structure.py' board.
        self.case_x = 0
        self.case_y = 0
        # pylint: disable=C0103
        self.x, self.y = initial_position

        # Read the structure to interact with the differnts sprites types.
        with open("structure.py") as fd:
            self.structure = fd.readlines()

    def move(self, direction):
        """Function that allow the player to move"""
        if direction == pygame_locals.K_RIGHT:
            # Check if we are against the window frame before to allow the move.
            if self.x < (window_width - 50):
                # Check if the next sprite is a wall or a ground before to allow the move.
                if self.structure[self.case_y][self.case_x + 1] != '1':
                    # Update the position in the structure grid.
                    self.case_x += 1
        elif direction == pygame_locals.K_LEFT:
            if self.x > 0:
                if self.structure[self.case_y][self.case_x - 1] != '1':
                    self.case_x -= 1
        elif direction == pygame_locals.K_UP:
            if self.y > 0:
                if self.structure[self.case_y - 1][self.case_x] != '1':
                    self.case_y -= 1
        elif direction == pygame_locals.K_DOWN:
            # In this case we need to avoid to move the player in the inventory line.
            # So -100 instead of -50 pixels
            if self.y < (window_height - 100):
                if self.structure[self.case_y + 1][self.case_x] != '1':
                    self.case_y += 1

        self.x = self.case_x * sprite_size
        self.y = self.case_y * sprite_size


class Keeper(Player):

    """This descendant class only manage the keeper position in the maze.
    He may have be handled in the Labyrinth class.
    However this option could permit to work on a game enhancement or an add-on.
    The keeper may get an aggressive behaviour. Or for a multi-player project."""


def main():
    """Main loop for the game"""
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("FREE MACGYVER")

    maze = Maze(window)
    macgyver = Player("images/MacGyver.png")
    keeper = Keeper("images/keeper.png", initial_position=(700, 700))

    # Allow the player to move faster if he keeps the button pushed.
    pygame.key.set_repeat(400, 30)

    # Main loop containing the game code.
    # It allows to run the game as long as the player doesn't quit.
    keep_going = 1
    while keep_going:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == pygame_locals.QUIT:
                keep_going = 0

            mac_pos = macgyver.position

            # This condition allow the player to move but stop the movement after having faced
            # the keeper, which induced the end of the game.
            if event.type == pygame_locals.KEYDOWN and mac_pos != (700, 700):
                macgyver.move(event.key)

            if maze.is_sprite_item(mac_pos):
                item = maze.item_references[mac_pos]
                maze.inventory.append(item)
                maze.manage_inventory(mac_pos)

            maze.display_structure()
            maze.display_items()
            maze.choose_text(mac_pos)

            window.blit(keeper.icon, keeper.position)
            window.blit(macgyver.icon, macgyver.position)

            pygame.display.flip()


if __name__ == '__main__':
    main()
