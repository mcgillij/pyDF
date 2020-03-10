#! /usr/bin/env python

import pygame_sdl2
pygame_sdl2.import_as_pygame()
#from pygame.locals import KEYDOWN
class EzMenu:

    def __init__(self, options):
    #def __init__(self, *options):
        """Initialise the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""

        self.options = options
        self.x = 0
        self.y = 0
        self.font = pygame_sdl2.font.Font(None, 32)
        self.selected = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.options) * self.font.get_height()
        for o in self.options:
            text = o.name
            #text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    def draw(self, surface):
        """Draw the menu to the surface."""
        i = 0
        for o in self.options:
            if i == self.selected:
                clr = self.hcolor
            else:
                clr = self.color
            text = o.name
            #text = o[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, (self.x, self.y + i * self.font.get_height()))
            i += 1
            
    def update(self, event):
        print(str(event))
        keymods = pygame_sdl2.key.get_mods()
        """Update the menu and get input for the menu."""
        if event.type == pygame_sdl2.KEYDOWN:
            if event.key == pygame_sdl2.K_DOWN and keymods & pygame_sdl2.KMOD_LALT:
                print("This is being called")
                self.selected += 1
            if event.key == pygame_sdl2.K_UP and keymods & pygame_sdl2.KMOD_LALT:
                print("This is totally not being called")
                self.selected -= 1
            if event.key == pygame_sdl2.K_RETURN:
                self.result(self.options[self.selected])# execute
                #self.options[self.option][1]() # execute
        if self.selected > len(self.options) - 1:
            self.selected = 0
        if self.selected < 0:
            self.selected = len(self.options) - 1
        print("options : " + str(len(self.options)))

    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.x = x
        self.y = y
        
    def set_font(self, font):
        """Set the font used for the menu."""
        self.font = font
        
    def set_highlight_color(self, color):
        """Set the highlight color"""
        self.hcolor = color
        
    def set_normal_color(self, color):
        """Set the normal color"""
        self.color = color
        
    def center_at(self, x, y):
        """Center the center of the menu at x,y"""
        self.x = x - (self.width / 2)
        self.y = y - (self.height / 2)
    def result(self, value):
        print(value)
        return value
