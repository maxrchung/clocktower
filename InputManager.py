import pygame
from pygame.locals import *
pygame.init()

class InputManager:
    def __init__(self):
        self.L_DOWN = False
        self.R_DOWN = False
        self.UP_DOWN = False
        self.SPACE_DOWN = False

    def update(self):
        # Use get_pressed() for holding down keys
        keys = pygame.key.get_pressed()
        self.L_DOWN = keys[K_LEFT]
        self.R_DOWN = keys[K_RIGHT]
        self.UP_DOWN = keys[K_UP]
        self.SPACE_DOWN = keys[K_SPACE]
