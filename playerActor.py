import pygame
import actor
import InputManager
import physicsManager
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
        self.checkState()

    def checkInputs(self):
        oldstate = str(self.currState)
        if self.input.L_DOWN:
            self.orientation = "left"
            if self.input.SPACE_DOWN:
                self.currState = "JUMP_LEFT"
            else:
                self.currState = "MOVE_LEFT"
        elif self.input.R_DOWN:
            self.orientation = "right"
            if self.input.SPACE_DOWN:
                self.currState = "JUMP_RIGHT"
            else:
                self.currState = "MOVE_RIGHT"
        elif self.input.SPACE_DOWN:
            self.currState = "JUMP_NEUTRAL"
        else:
            self.currState = "IDLE"

    def checkState(self):
        if self.currState == "MOVE_LEFT":
            self.accels['move'] = 12.0
            self.targetVelocities['move'] = actor.vector.Vector(-5.0, None)
        elif self.currState == "MOVE_RIGHT":
            self.accels['move'] = 12.0
            self.targetVelocities['move'] = actor.vector.Vector(5.0, None)
        elif self.currState == "JUMP_NEUTRAL":
            self.accels['jump'] = 200.0
            self.targetVelocities['jump'] = actor.vector.Vector(None, 5.0)
        elif self.currState == "IDLE":
            self.accels['move'] = 20.0
            self.targetVelocities['move'] = actor.vector.Vector(0.0, None)
            if 'jump' in self.accels:
                self.accels.pop('jump')
                self.targetVelocities.pop('jump')            
