try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
    import sys
    import os
    #from pygame.locals import *
    from time import time
    import pprint
    from loader import load_png
    import configparser, os
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)

class Mob(pygame_sdl2.sprite.Sprite):
    """ Mob class, generic class for a sprite """
    def __init__(self, position, tw):
        self.tw = tw
        config = configparser.ConfigParser()
        config.read_file(open('mob.cfg'))
        imageset = 'imagename' + str(self.tw)
        imagename = config.get('mob', imageset)
        self.image, self.rect = load_png(imagename)
        self.position = position
        self.miningskill = 5
        self.name = "Jimmy"
        self.surface = pygame_sdl2.transform.scale(self.image, (self.tw, self.tw))
        self.pathlines = []
        self.job = None
        self.skillcounter = 0
        self.carrying = None

    def pickupitem(self, item):
        self.carrying = item

    def __repr__(self):
        return self.name
