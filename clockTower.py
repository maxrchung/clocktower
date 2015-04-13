__author__ = 'Ira'
import time
import os
import pygame


class Hand:
    def __init__(self, surface):
        self.surface = surface
        self.image = pygame.image.load(os.path.join('Art', 'minuteHand.png')).convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        # current minute
        self.start_angle = 30
        self.current_angle_offset = 0
        # start the timer
        self.start_time = time.time()
        self.total_time = 300
        self.end_time = self.start_time + self.total_time

        # the angle of one minute on the clock
        self.minute_angle = 6


    def update(self):
        if self.start_time > self.end_time:
            print("ran out")
            return "END"  # TIMER RAN OUT
        self.current_time = self.end_time - time.time()

        self.current_angle_offset = 5 - self.current_time // 60 #self.total_time

        orig_rect = self.rect
        self.current_angle = self.start_angle - self.current_angle_offset*self.minute_angle
        rotated_image = pygame.transform.rotate(self.original_image, self.current_angle)
        rotated_rect = orig_rect.copy()
        rotated_rect.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rect).copy()

        self.image = rotated_image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        #self.surface.blit(self.background, (0,0))
        self.surface.blit(self.image, (608-38, 93))