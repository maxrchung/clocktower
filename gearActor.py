import pygame
import actor


class GearActor(actor.Actor):
    def __init__(self, pos, spritePath, useGravity, groups):
        # Call parent constructor
        actor.Actor.__init__(self, pos, spritePath, useGravity, groups)

    def rotateGear(self):
        ANGLE = 10
        self.image = pygame.transform.rotate(self.image, ANGLE)
        self.mask = pygame.mask.from_surface(self.image)