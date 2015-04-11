import pygame
import vector
from pygame.locals import *
class Actor(pygame.sprite.Sprite):
    def __init__(self, pos, spritePath, groups):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set a position for the Actor
        self.pos = pos
        # Set the sprite with the given image path. Make a mask as well
        # for collision detection
        self.image = pygame.image.load(spritePath).convert()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        # use pygame.sprite.collide_mask()
        # usage: collide_mask(SpriteLeft, SpriteRight) -> point
        
        # Set some default forces and velocity
        self.accels = {'gravity':vector.Vector(0.0,-9.8)}
        self.velocity = vector.Vector(0.0,0.0)
        
        # Add sprite into the specified groups. 
        self.add(groups);

    def updatePhysics(self, timeSinceLastUpdate):
        if timeSinceLastUpdate > 0.0:
            # for each acceleration, add to the current velocity
            for a in self.accels.values():
                self.velocity += a/timeSinceLastUpdate
            # update the current position based on velocity
            self.pos += self.velocity
            self.rect.move_ip(self.velocity.x, -1*self.velocity.y)
