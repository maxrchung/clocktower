import pygame
import vector
from pygame.locals import *
class Actor(pygame.sprite.Sprite):
    def __init__(self, pos, spritePath, useGravity, groups):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set a position for the Actor
        self.pos = pos
        # Set the sprite with the given image path. Make a mask as well
        # for collision detection
        self.image = pygame.image.load(spritePath).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos.x, pos.y)
        self.mask = pygame.mask.from_surface(self.image)
        # use pygame.sprite.collide_mask()
        # usage: collide_mask(SpriteLeft, SpriteRight) -> point
        
        # Set some default forces and velocity
        self.accels = {}
        self.targetVelocities = {}
        self.velocity = vector.Vector(0.0,0.0)
        if useGravity:
            self.accels['gravity'] = 4.0
            self.targetVelocities['gravity'] = vector.Vector(0.0, -12.0)
        
        # Add sprite into the specified groups. 
        self.add(groups);

    def updatePhysics(self, timeSinceLastUpdate):
        if timeSinceLastUpdate > 0.0:
            # for each acceleration, move towards the target velocity
            # at the rate of acceleration
            for k in self.accels.keys():
                # get acceleration and scale by time since last update
                increment = self.accels[k]/timeSinceLastUpdate
                # then move towards the target velocity
                self.velocity.moveTowards(self.targetVelocities[k], increment)
            # update the current position based on velocity
            self.moveActor(self.velocity.x, self.velocity.y)

    def moveActor(self, x, y):
        self.pos += vector.Vector(x, y)
        self.rect.move_ip(x, -1*y)