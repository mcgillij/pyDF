try:
    import sys
    import pygame
    from pygame.locals import *
    from item import Item
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)


class Room(object):
    """ Room class, generic class for a tile """

    def __init__(self, value, type, list):
        self.value = value
        self.type = type
        self.roomtiles = list
