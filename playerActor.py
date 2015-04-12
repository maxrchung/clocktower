import pygame
import actor
import InputManager
from pygame.locals import *
 
class PlayerActor(actor.Actor):
    def __init__(self, pos, spritePath, groups):
        # Call the parent class (Actor) constructor
        actor.Actor.__init__(self, pos, spritePath, True, groups)
        # TODO: add animator
        self.currState = "IDLE"
        self.orientation = "right"
        # create an input manager
        self.input = InputManager.InputManager()

    def update(self):
        # update the input manager
        self.input.update()
        # do state transitions as needed
        self.checkInputs()

    def checkInputs(self):
        
        oldstate = str(self.currState)
        # left
        if self.input.L_DOWN:
            self.orientation = "left"
            # left jump
            if self.input.SPACE_DOWN:
                self.currState = "JUMP_LEFT"
            else:
                self.currState = "MOVE_LEFT"
        # right
        elif self.input.R_DOWN:
            self.orientation = "right"
            # right jump
            if self.input.SPACE_DOWN:
                self.currState = "JUMP_RIGHT"
            else:
                self.currState = "MOVE_LEFT"
        # stationary jump
        elif self.input.SPACE_DOWN:
            self.currState = "JUMP_NEUTRAL"
        else:
            self.currState = "IDLE"
            print(self.currState)
            
