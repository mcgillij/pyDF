try:
    import pygame, random, sys
    import pygame.font
    from pygame.locals import *
    import os
except ImportError as err:
    print("couldn't load module. {err}")
    sys.exit(2)


def load_font(name, size):
    """Load up a font file, or try to use the default None(system font)"""
    fullname = os.path.join('data', name)
    try:
        font = pygame.font.Font(fullname, size)
    except pygame.error as message:
        print(f'Cannot load font file: {fullname}')
    else:
        font = pygame.font.SysFont(None, size)
    return font


def load_sound(name):
    """ Load the sound file from the data directory, return sound """
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print(f'Cannot load sound file: {fullname}')
        raise SystemExit(message)
    return sound


def load_png(name):
    """ Load image and return image object """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print(f'Cannot load image: {fullname}')
        raise SystemExit(message)
    return image, image.get_rect()
