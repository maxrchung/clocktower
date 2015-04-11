__author__ = 'Ira'
import pygame
import os


class Animation:
    def __init__(self, spritesheet_path, rectangle, info_dict):
        """
        :param spritesheet_path: a list of folder/file names that are the pathway to the raw image file
        :param rectangle: rectangle object
        :param info_dict: "statename" --> ( rownumber, frame_count ); where rownumber starts at 0
        // mine:
        load sprite sheet
        cut up the image into equal rects
        store in memory
        every time the game says DRAWSPRITE -- draw the one you're currently on
        every time to update have that switch to the next frame
        """
        self._load_image(spritesheet_path)

        self._states = {}

        self._current_state = ""            # current state
        self._current_frameindex = 0

        #self._loop = True           # keep looping ?

        self._rectangle = rectangle

        for (state_name, info) in info_dict.items():
            # info == ( rownumber, framecount )
            self._create_state(state_name, info[0], info[1])

    def _frame_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        frame = pygame.Surface(rect.size).convert()
        frame.blit(self._spritesheet, (0, 0), rect)
        return frame

    def _frames_at(self, rectangles):
        return [self._frame_at(rectangle) for rectangle in rectangles]

    def _create_state(self, state_name, row_number, frame_count):
        frames = []
        for col_number in range(frame_count):
            frames[col_number] = pygame.Rect( self._rectangle.x*col_number, row_number, self._rectangle.x*(col_number+1), row_number+1 )

        self._states[state_name] = (frame_count, frames)
        return

    def _load_image(self, spritesheet_path):
        try:
            self._spritesheet = pygame.image.load(os.path.join(*spritesheet_path)).convert()

        except:
            print ('An error has occurred while the game was loading the image ', spritesheet_path)

    def _next_frameindex(self, frame_count):
        """
        :return: index of the next frame relative to current; loops to the 0th frame at the end
        """
        if (self._current_frameindex + 1) == frame_count:
            return 0
        else:
            return self._current_frameindex + 1

    def get_frame(self, actor_state):
        """
        :param actor_state: the string specifying state you want me to switch to/keep if the same
        :return: the according frame (next in line if the state is the same, first in line if the state is new)
        """
        if self._current_state == actor_state:  # same state as before
            self._current_frameindex = self._next_frameindex()

        else:                                   # new state, gotta update
            self._current_state = actor_state
            self._current_frameindex = 0

        return self._states[self._current_state][1][self._current_frameindex]




if __name__ == "__main__":
    #rect = pygame.Rect(0, 0, 96, 144)
    mine = Animation(["idleLeft.png"])
    mine._frame_at(0, 0, 96, 144)