__author__ = 'Ira'
import time
import os
import pygame


class Hand:
    def __init__(self, surface):
        self.surface = surface
        # init the minute hand
        self.image = pygame.image.load(os.path.join('Art', 'minuteHand.png')).convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()

        # init the hour hand
        self.hour_image = pygame.image.load(os.path.join('Art', 'hourHand.png')).convert_alpha()
        self.hour_original_image = self.hour_image.copy()
        self.hour_rect = self.image.get_rect()

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
            rotated_hourimage = pygame.transform.rotate(self.hour_image, -6)
            rotated_rect = self.hour_image.get_rect().copy()
            rotated_rect.center = rotated_hourimage.get_rect().center
            self.hour_image = rotated_hourimage.subsurface(rotated_rect).copy()
            self.draw()
            return "END"  # TIMER RAN OUT
        self.current_time = self.end_time - time.time()

        self.hour_image = pygame.transform.rotate(self.hour_original_image, 8)

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
        self.surface.blit(self.image, (608-40, 93))
        self.surface.blit(self.hour_image, (608-42, 93))
