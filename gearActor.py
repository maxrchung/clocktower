import pygame
import actor


class GearActor(actor.Actor):
    def __init__(self, pos, spritePath, useGravity, groups):
        # Call parent constructor
        actor.Actor.__init__(self, pos, spritePath, useGravity, groups)
        self.original_image = pygame.Surface(self.image)
        self.current_angle = 0

    def rotateGear(self):
        OFFSET = 10

        if self.current_angle < 360:
            orig_rect = self.rect
            rotated_image = pygame.transform.rotate(self.original_image, OFFSET)
            rotated_rect = orig_rect.copy()
            rotated_rect.center = rotated_image.get_rect().center
            rotated_image = rotated_image.subsurface(rotated_rect).copy()

            self.image = rotated_image
            self.mask = pygame.mask.from_surface(self.image)
            self.current_angle += OFFSET
        else:
            self.image = self.original_image