try:

    import pygame
    import sys
    import os
    from pygame.locals import *
    from time import time
    import pprint
    import loader
    from configparser import ConfigParser
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

class Item(pygame.sprite.Sprite):
    """ Item class, generic class for a sprite """
    def __init__(self, name, tw):
        self.tw = tw
        config = ConfigParser()
        config.read_file(open('config/item.cfg'))
        sectionname = 'imagename' + str(self.tw)
        self.movable = True # set this to false to make unmovable items.
        self.selected = False
        self.inqueue = False
        
        imagename = config.get(name, sectionname)
        self.image, self.rect = loader.load_png(imagename)
        self.name = name
        self.surface = pygame.transform.scale(self.image, (self.tw, self.tw))
    def __repr__(self):
        return self.name
