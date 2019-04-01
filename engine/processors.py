import pygame
from esper import Processor

from .components import Velocity, Renderable


"""
Processors, also commonly known as "Systems", are where all processing logic is defined and executed. 
All Processors must inherit from the esper.Processor class, and have a method called process. 
Other than that, there are no restrictions. All Processors will have access to the World instance, 
to allow easy querying of Components. 



    class MovementProcessor(esper.Processor):
        def __init__(self):
            super().__init__()
    
        def process(self):
            for ent, (vel, pos) in self.world.get_components(Velocity, Position):
                pos.x += vel.x
                pos.y += vel.y

In the above code, you can see the standard usage of the World.get_components() method. This method allows efficient 
iteration over all Entities that contain the specified Component types. You also get a reference to the Entity ID for 
the current pair of Velocity/Position Components, in case you should need it. For example, you may have a Processor 
that will delete certain Entites. You could add these Entity IDs to a list, and call the self.world.delete_entity() 
method on them after you're done iterating over the Components. 

"""


class RenderProcessor(Processor):
    def __init__(self, window, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        # Clear the window:
        self.window.fill(self.clear_color)
        # This will iterate over every Entity that has this Component, and blit it:
        for ent, rend in self.world.get_component(Renderable):
            self.window.blit(rend.image, (rend.x, rend.y))
        # Flip the framebuffers
        pygame.display.flip()


class MovementProcessor(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def process(self):
        # This will iterate over every Entity that has BOTH of these components:
        for ent, (vel, rend) in self.world.get_components(Velocity, Renderable):
            # Update the Renderable Component's position by it's Velocity:
            rend.x += vel.x
            rend.y += vel.y
            # An example of keeping the sprite inside screen boundaries. Basically,
            # adjust the position back inside screen boundaries if it tries to go outside:
            rend.x = max(self.minx, rend.x)
            rend.y = max(self.miny, rend.y)
            rend.x = min(self.maxx - rend.w, rend.x)
            rend.y = min(self.maxy - rend.h, rend.y)



