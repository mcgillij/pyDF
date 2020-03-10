#!C:\python26\python.exe
try:
    import pygame_sdl2
    #from pygame_sdl2 import KEYDOWN, KESCAPE, QUIT, RESIZABLE
    pygame_sdl2.import_as_pygame()
    import sys
    #from pygame.locals import *
except ImportError as err:
    print("couldn't load module, %s" % (err))
    sys.exit(2)

class Intro(object):
    """ This will probably be adjusted to be usable for any text screen
        but for now I will use it just for the intro / instructions screen """
    def __init__(self):
        self.title = "PyDF"
        self.textcolor = (255, 255, 255)
        if not pygame_sdl2.font.get_init():
            pygame_sdl2.font.init()
        self.arialFnt = pygame_sdl2.font.SysFont('Arial', 16)

    def drawText(self, text, surface, x, y):
        textobj = self.arialFnt.render(text, 1, self.textcolor)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def waitForKey(self):
        running = True;
        while True:
            for event in pygame_sdl2.event.get():
                if event.type == pygame_sdl2.QUIT:
                    running = False
                if event.type == pygame_sdl2.KEYDOWN:
                    if event.key == pygame_sdl2.K_ESCAPE: # pressing escape quits
                        running = False
                    return

if __name__ == '__main__':
    pygame_sdl2.init()
    screen = pygame_sdl2.display.set_mode((640, 480), pygame_sdl2.RESIZABLE)
    intro = Intro()
    intro.drawText("hi", screen, 10, 10)
    pygame_sdl2.display.update()
    intro.waitForKey()
