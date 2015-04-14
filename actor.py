import pygame
import vector
import animation
import os
from pygame.locals import *

class Actor(pygame.sprite.Sprite):
    def __init__(self, pos, animation, useGravity, radius, groups, id=None):
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
        self.center = self.rect.center
        self.radius = radius

        # Set some default forces and velocity
        self.accels = {}
        self.targetVelocities = {}
        self.velocity = vector.Vector(0.0,0.0)
        if useGravity:
            self.accels['gravity'] = 4.0
            self.targetVelocities['gravity'] = vector.Vector(None, -8.0)

        # Will be specified by the inherited classes
        self.tear = None
        self.id = id
        if self.id == "LADDER_BOTTOM":
            self.tearpos = (self.pos.x - 24, self.pos.y)
            self.tear = pygame.image.load(os.path.join('Art', 'ladderBottomTear.png')).convert_alpha()
        elif self.id == 'LADDER_TOP':
            self.tearpos = (self.pos.x - 24, self.pos.y)
            self.tear = pygame.image.load(os.path.join('Art', 'ladderTopTear.png')).convert_alpha()


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
                if k in self.targetVelocities:
                    self.velocity.moveTowards(self.targetVelocities[k], increment)
            # update the current position based on velocity
            self.moveActor(self.velocity.x, self.velocity.y)

    def moveActor(self, x, y):
        self.pos.x += x
        self.pos.y -= y
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.center = self.rect.center
        #self.rect.move_ip(x, y)

    def moveTo(self, x, y):
        self.pos.x = x
        self.pos.y = y
        self.rect.x = x
        self.rect.y = y
        self.center = self.rect.center

    def updateAnimation(self, actor_state):
        self.animator.update_frame(actor_state)
        self.image = self.animator.get_current_frame()
