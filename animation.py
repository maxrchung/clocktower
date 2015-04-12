__author__ = 'Ira'
import pygame
import os
from pygame.locals import *

class Animation:
    def __init__(self, spritesheet_path, rectangle, info_dict):
        """
        :param spritesheet_path: a list of folder/file names that are the pathway to the raw image file
        :param rectangle: rectangle object
        :param info_dict: "statename" --> ( rownumber, frame_count ); where rownumber starts at 0

        """
        self._load_image(spritesheet_path)

        self._states = {}

        self._current_state = ""
        self._current_frameindex = 0

        self._rectangle = rectangle

        for (state_name, info) in info_dict.items():
            self._create_state(state_name, info[0], info[1])

    def _frame_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        frame = pygame.Surface(rect.size).convert()
        frame.blit(self._spritesheet, (0, 0), rect)
        return frame

#    def _frames_at(self, rectangles):
#        return [self._frame_at(rectangle) for rectangle in rectangles]

    def _create_state(self, state_name, row_number, frame_count):
        frames = []
        masks = []
        rects = []

        for col_number in range(frame_count):
            rects.append(pygame.Rect(self._rectangle.x*col_number, self._rectangle.y*row_number,
                                     self._rectangle.x*(col_number+1), self._rectangle.y*(row_number+1)))

            frames.append(self._frame_at(rects[col_number]))
            masks.append(pygame.mask.from_surface(frames[col_number]))

        """
        for col_number in range(frame_count):
            #print(col_number)
            frames = self._frames_at( [] )
            #frames.append(pygame.Rect( self._rectangle.x*col_number, row_number, self._rectangle.x*(col_number+1), row_number+1 ))
            masks.append(pygame.mask.from_surface(frames[col_number]))
        """

        self._states[state_name] = (frame_count, frames, masks)
        return

    def _load_image(self, spritesheet_path):
        self._spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

    def _next_frameindex(self, frame_count):
        """
        :return: index of the next frame relative to current; loops to the 0th frame at the end
        """
        if (self._current_frameindex + 1) == frame_count:
            return 0
        else:
            return self._current_frameindex + 1

    def update_frame(self, actor_state):
        """
        :param actor_state: string specifying the state
        :return: None, just updates the things internally
        """
        if self._current_state == actor_state:  # same state as before
            self._current_frameindex = self._next_frameindex()

        else:                                   # new state, gotta update
            self._current_state = actor_state
            self._current_frameindex = 0

    def get_current_frame(self):
        """
        :param actor_state: the string specifying state you want me to switch to/keep if the same
        :return: the according frame (next in line if the state is the same, first in line if the state is new)
        """
        return self._states[self._current_state][1][self._current_frameindex]

    def get_current_mask(self):
        return self._states[self._current_state][2][self._current_frameindex]




if __name__ == "__main__":
    pygame.init()
    rect = pygame.Rect(0, 0, 96, 144)
    size = 480, 640
    _display_surf = pygame.display.set_mode(size, pygame.SWSURFACE)

    info = {"check": (0, 4)}
    mine = Animation(os.path.join('Art', 'idleLeft.png'), rect, info)
    mine._frame_at(pygame.Rect(0, 0, 96, 144))
