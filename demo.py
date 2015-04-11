import pygame
import os
import actor
import vector
import physicsManager
from pygame.locals import *
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 480, 640
        # Need a clock to scale physics vectors
        self.clock = pygame.time.Clock()
        # Keep a group of renderable actors
        self.renderables = pygame.sprite.LayeredUpdates()
        # Keep a group of static colliders
        self.staticColliders = pygame.sprite.Group()
        # Temporary background
        self.background = pygame.Surface((480, 640))
        self.background.fill((0, 0, 0))
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.SWSURFACE)
        self._running = True
        # create actors
        # 0: player actor. uses gravity, part of renderables
        # 1: static actor. doesn't use gravity, part of renderables and staticColliders
        self.actors = [actor.Actor(vector.Vector(0, 0), os.path.join('Art', 'idleLeft.png'), True, (self.renderables)),
                       actor.Actor(vector.Vector(0, 500), os.path.join('Art', 'idleRight.png'), False, (self.renderables, self.staticColliders))]
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        # update at 60 fps
        self.clock.tick(60)
        # update physics for each actor in the game
        for a in self.actors:
            a.updatePhysics(self.clock.get_time())
        # check for collisions
        collisionList = physicsManager.checkCollisionAgainstGroup(self.actors[0], self.staticColliders)
        # if there were collisions, resolve intersections
        for collider in collisionList.keys():
            physicsManager.resolveIntersection(self.actors[0], collider)
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
