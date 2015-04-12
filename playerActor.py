import pygame
import actor
import InputManager
import soundManager

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
        self.sound = soundManager.SoundManager()
        
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
                self.sound.pauseMusic()
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
        print(self.currState)

    def checkState(self):
        if self.currState == "MOVE_LEFT":
            self.accels['move'] = 4.0
            self.targetVelocities['move'] = actor.vector.Vector(-12.0, None)
        elif self.currState == "MOVE_RIGHT":
            self.accels['move'] = 4.0
            self.targetVelocities['move'] = actor.vector.Vector(12.0, None)
        elif self.currState == "JUMP_NEUTRAL":
<<<<<<< HEAD
            self.accels['jump'] = 4.0
            self.targetVelocities['jump'] = actor.vector.Vector(0.0, 12.0)
=======
            self.accels['jump'] = 20.0
            self.targetVelocities['jump'] = actor.vector.Vector(None, 24.0)
>>>>>>> 3a1543ae49c373d93a847d60690e90b768435e93
        elif self.currState == "IDLE":
            self.accels['move'] = 0.0
            self.targetVelocities['move'] = actor.vector.Vector(0.0, 0.0)
            if 'jump' in self.accels:
                self.accels.pop('jump')
                self.targetVelocities.pop('jump')            
