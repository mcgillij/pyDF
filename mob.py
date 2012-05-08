try:
    import pygame
    import sys
    import os
    from pygame.locals import *
    from time import time
    import pprint
    import loader
    import ConfigParser, os
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

class Mob(pygame.sprite.Sprite):
    """ Mob class, generic class for a sprite """
    def __init__(self, position, tw):
        self.tw = tw
        config = ConfigParser.ConfigParser()
        config.readfp(open('mob.cfg'))
        imageset = 'imagename' + str(self.tw)
        imagename = config.get('mob', imageset)
        self.image, self.rect = loader.load_png(imagename)
        self.position = position
        self.miningskill = 5
        self.name = "Jimmy"
        self.surface = pygame.transform.scale(self.image, (self.tw, self.tw))
        self.pathlines = []
        self.job = None
        self.skillcounter = 0
        self.carrying = None

    def pickupitem(self, item):
        self.carrying = item

    def __repr__(self):
        return self.name
