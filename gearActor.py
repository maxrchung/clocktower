import pygame
import actor
import copy

class GearActor(actor.Actor):
    def __init__(self, pos, animation, clockwise, groups):
        # Call parent constructor
        actor.Actor.__init__(self, pos, animation, False, groups)
        self.original_image = copy.copy(self.image)
        self.current_angle = 0
        self.clockwise = clockwise
        self.timer = 0

    def rotateGear(self):
        OFFSET = -3
        if not self.clockwise:
            OFFSET *= -1
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
                self.current_angle += OFFSET
            else:
                self.image = copy.copy(self.original_image)
                self.current_angle = 0
        else:
            self.timer += 1
