try:
    import pygame
    import sys

except ImportError as err:
    print("couldn't load module, %s" % (err))
    sys.exit(2)


class Intro:
    """This will probably be adjusted to be usable for any text screen
    but for now I will use it just for the intro / instructions screen"""

    running = True

    def __init__(self):
        self.title = "PyDF"
        self.textcolor = (255, 255, 255)
        if not pygame.font.get_init():
            pygame.font.init()
        self.arialFnt = pygame.font.SysFont("Arial", 16)

    def drawText(self, text, surface, x, y):
        textobj = self.arialFnt.render(text, 1, self.textcolor)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def waitForKey(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # pressing escape quits
                        self.running = False
                    return


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    intro = Intro()
    intro.drawText("hi", screen, 10, 10)
    pygame.display.update()
    intro.waitForKey()
