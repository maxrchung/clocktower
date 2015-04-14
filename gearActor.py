import pygame
import actor
import os
import vector
import tempTrig
import random

class GearActor(actor.Actor):
    def __init__(self, pos, animation, clockwise, radius, groups, id=None):
        # Call parent constructor
        actor.Actor.__init__(self, pos, animation, False, radius, groups)
        self.original_image = self.image.copy()
        self.current_angle = 0
        self.clockwise = clockwise
        self.timer = 0
        if id == "SMALL":
            self.tearpos = (self.pos.x - 24, self.pos.y - 24)
            self.tear = pygame.image.load(os.path.join('Art', 'verticalGear1Tear.png')).convert_alpha()
        elif id == "MEDIUM":
            self.tearpos = (self.pos.x - 24, self.pos.y - 24)
            self.tear = pygame.image.load(os.path.join('Art', 'verticalGear2Tear.png')).convert_alpha()
        elif id == "LARGE":
            self.tearpos = (self.pos.x - 24, self.pos.y - 24)
            self.tear = pygame.image.load(os.path.join('Art', 'verticalGear3Tear.png')).convert_alpha()
        self.OFFSET = random.randint(1, 4)
        if self.clockwise:
            self.OFFSET *= -1
        self.offsetVector = (vector.Vector(tempTrig.get_center_x(radius, self.OFFSET), tempTrig.get_center_y(radius, self.OFFSET)) * self.OFFSET).get_norm()

    def rotateGear(self):
        if self.timer == 1:
            self.timer = 0
            if self.current_angle < 360:
                orig_rect = self.rect
                rotated_image = pygame.transform.rotate(self.original_image, self.current_angle)
                rotated_rect = orig_rect.copy()
                rotated_rect.center = rotated_image.get_rect().center
                rotated_image = rotated_image.subsurface(rotated_rect).copy()

                self.image = rotated_image
                self.mask = pygame.mask.from_surface(self.image)
                self.current_angle += self.OFFSET
            else:
                self.image = self.original_image.copy()
                self.current_angle = 0
        else:
            self.timer += 1
