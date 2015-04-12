import pygame
import actor
import InputManager
import physicsManager
from pygame.locals import *
 
class PlayerActor(actor.Actor):
    def __init__(self, pos, animation, groups):
        # Call the parent class (Actor) constructor
        actor.Actor.__init__(self, pos, animation, True, groups)
        self.currState = "IDLE"
        self.prev_orientation = "Right"
        self.curr_orientation = "Right"
        # create an input manager
        self.input = InputManager.InputManager()
        
    def update(self):
        # update the input manager
        self.input.update()
        # do state transitions as needed
        self.checkInputs()
        self.checkState()
        self.checkAnimation()

    def checkInputs(self):
        oldstate = str(self.currState)
        if self.input.L_DOWN:
            self.prev_orientation, self.curr_orientation = self.curr_orientation, "Left"
            if self.input.SPACE_DOWN:
                self.currState = "JUMP_LEFT"
            else:
                self.currState = "MOVE_LEFT"
        elif self.input.R_DOWN:
            self.prev_orientation, self.curr_orientation = self.curr_orientation, "Right"
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

    def checkAnimation(self):
        if self.curr_orientation != self.prev_orientation: # case: Turned
            timer = 0
            for i in range(7):
                if timer == 5:
                    self.updateAnimation("turnTo" + self.curr_orientation)
                    timer = 0
                else:
                    timer += 1
            #self.updateAnimation("idleLeft")

        actor_state = ""
        if self.currState == "IDLE":
            actor_state = "idle" + self.curr_orientation

        else:
            actor_state = "move" + self.curr_orientation

        self.updateAnimation(actor_state)




