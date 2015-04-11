import pygame
import os
import actor
import vector
from pygame.locals import *
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 480, 640
        # Need a clock to scale physics vectors
        self.clock = pygame.time.Clock()
        # Keep a layer of renderable sprites
        self.renderables = pygame.sprite.LayeredUpdates()
        # Temporary background
        self.background = pygame.Surface((480, 640))
        self.background.fill((0, 0, 0))
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.SWSURFACE)
        self._running = True
        self.actors = [actor.Actor(vector.Vector(0, 0), os.path.join('data', 'sprite.png'), self.renderables)]
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        self.clock.tick(60)
        for a in self.actors:
            a.updatePhysics(self.clock.get_time())
    def on_render(self):
        # Draw everything in the LayeredUpdates group
        dirty = self.renderables.draw(self._display_surf)
        # Update the window
        pygame.display.update(dirty)
        # Clear the previously rendered stuff
        self.renderables.clear(self._display_surf, self.background)
   
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
