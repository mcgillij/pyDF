import pygame
import sys
from esper import World

from .processors import RenderProcessor


# https://github.com/benmoran56/esper/blob/master/examples/pygame_example.py


class Game:
    def __init__(self):
        pygame.init()
        self.resolution = (800, 600)  # TODO: configurable
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(self.resolution)
        self.running = True
        self.world = GameWorld(self)
        self.FPS = 60

    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # Here is a way to directly access a specific Entity's
                        # Velocity Component's attribute (y) without making a
                        # temporary variable.
                        # world.component_for_entity(player, Velocity).x = -3
                        pass
                    elif event.key == pygame.K_RIGHT:
                        # For clarity, here is an alternate way in which a
                        # temporary variable is created and modified. The previous
                        # way above is recommended instead.
                        # player_velocity_component = world.component_for_entity(player, Velocity)
                        # player_velocity_component.x = 3
                        pass
                    elif event.key == pygame.K_UP:
                        # world.component_for_entity(player, Velocity).y = -3
                        pass
                    elif event.key == pygame.K_DOWN:
                        # world.component_for_entity(player, Velocity).y = 3
                        pass
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        # world.component_for_entity(player, Velocity).x = 0
                        pass
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        # world.component_for_entity(player, Velocity).y = 0
                        pass

            # A single call to world.process() will update all Processors:
            self.world.process()
            self.clock.tick(self.FPS)
        pygame.quit()
        sys.quit()

    pass


class GameWorld(World):
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.add_processor(RenderProcessor(window=self.game.window))


if __name__ == '__main__':
    print('TODO: need to create test scenario or call main game file..')
