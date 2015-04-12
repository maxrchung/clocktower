import pygame
import vector
import animation
from pygame.locals import *
class Actor(pygame.sprite.Sprite):
    def __init__(self, pos, animation, useGravity, groups):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set a position for the Actor
        self.pos = pos
        # Assign animator and get initial image and mask
        # from the animator
        self.animator = animation
        self.image = animation.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos.x, pos.y)
        self.mask = animation.get_current_mask()

        # use pygame.sprite.collide_mask()
        # usage: collide_mask(SpriteLeft, SpriteRight) -> point
        # Set some default forces and velocity
        self.accels = {}
        self.targetVelocities = {}
        self.velocity = vector.Vector(0.0,0.0)
        if useGravity:
            self.accels['gravity'] = 4.0
            self.targetVelocities['gravity'] = vector.Vector(None, -12.0)
        
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

    def updateAnimation(self, actor_state):
        self.animator.update_frame(actor_state)
        self.image = self.animator.get_current_frame()
        self.mask = self.animator.get_current_mask()
