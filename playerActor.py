import pygame
import actor
import InputManager
import physicsManager
import os
import soundManager
from pygame.locals import *
 
class PlayerActor(actor.Actor):
    def __init__(self, pos, animation, radius, groups):
        # Call the parent class (Actor) constructor
        actor.Actor.__init__(self, pos, animation, True, radius, groups)
        self.currState = "IDLE"
        self.prev_orientation = "Right"
        self.curr_orientation = "Right"
        # create an input manager
        self.input = InputManager.InputManager()
        self.timer = 0
        self.turning = False
        self.jumping = False
        # Sound Effect
        self.sound = soundManager.SoundManager()

        self.tearRight = pygame.image.load(os.path.join('Art', 'idleTearRight.png')).convert_alpha()
        self.tearRight = pygame.transform.smoothscale(self.tearRight, (88,132))
        self.tearLeft = pygame.image.load(os.path.join('Art', 'idleTearLeft.png')).convert_alpha()
        self.tearLeft = pygame.transform.smoothscale(self.tearLeft, (88,132))

        self.tear = self.tearRight

    def update(self):
        # update the input manager
        self.input.update()
        self.tearpos = (self.pos.x - 9, self.pos.y - 8)
        # do state transitions as needed
        #self.checkInputs()
        #self.checkState()
        self.doMove()
        self.doJump()
        self.checkAnimation()

    def doMove(self):
        if self.input.L_DOWN:
            self.accels['move'] = 10.0
            self.targetVelocities['move'] = actor.vector.Vector(-3.0, None)
            self.prev_orientation = self.curr_orientation
            self.tear = self.tearLeft
            self.curr_orientation = "Left"
        elif self.input.R_DOWN:
            self.accels['move'] = 10.0
            self.targetVelocities['move'] = actor.vector.Vector(3.0, None)
            self.prev_orientation = self.curr_orientation
            self.tear = self.tearRight
            self.curr_orientation = "Right"
        else:
            self.accels['move'] = 7.0
            self.targetVelocities['move'] = actor.vector.Vector(0.0, None)

    def doJump(self):
        if self.input.SPACE_DOWN and not self.jumping:
            self.jumping = True
            self.velocity.y = 6.0
            self.sound.playSoundEffect("Jumping.wav")
        else:
            self.targetVelocities['jump'] = actor.vector.Vector(None, None)
            
    def checkAnimation(self):
        if self.curr_orientation != self.prev_orientation: # case: Turned
            self.timer = 0
            self.turning = True
        if self.turning and self.timer < 7:
            self.updateAnimation("turnTo" + self.curr_orientation)
            self.timer += 1
        elif (self.input.L_DOWN or self.input.R_DOWN) and not self.jumping:
            self.updateAnimation("move" + self.curr_orientation)
        else:
            self.updateAnimation("idle" + self.curr_orientation)
'''
        if self.timer in (2, 4):
            if self.turning != -1:
                if self.turning == 6:
                    self.turning = -1
                else:
                    self.updateAnimation("turnTo" + self.curr_orientation)
                    self.turning += 1
        if self.timer == 4:
            actor_state = ""
            if self.currState == "IDLE":
                actor_state = "idle" + self.curr_orientation
            else:
                actor_state = "move" + self.curr_orientation
            self.updateAnimation(actor_state)
            self.timer = 0
        else:
            self.timer += 1
            '''
'''
    def checkInputs(self):
        oldstate = str(self.currState)

        if self.jumping:
            self.currState = "JNORM"
            if self.input.L_DOWN:
                self.prev_orientation, self.curr_orientation = self.curr_orientation, "Left"
                self.currState = "JUMP_LEFT"
                #self.currState = "MOVE_LEFT"

            if self.input.R_DOWN:
                self.prev_orientation, self.curr_orientation = self.curr_orientation, "Right"
                self.currState = "JUMP_RIGHT"
                #self.currState = "MOVE_RIGHT"

            elif self.input.SPACE_DOWN:
                pass

        else:
            if self.input.L_DOWN:
                self.prev_orientation, self.curr_orientation = self.curr_orientation, "Left"
                self.currState = "MOVE_LEFT"

            if self.input.R_DOWN:
                self.prev_orientation, self.curr_orientation = self.curr_orientation, "Right"
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

        elif self.jumping:
            #=========
            if self.currState == "JUMP_LEFT":
                #self.accels['move'] = 16.0
                self.targetVelocities['jump'] = actor.vector.Vector(-5.0, 3.0)
            elif self.currState == "JUMP_RIGHT":
                #self.accels['move'] = 16.0
                self.targetVelocities['jump'] = actor.vector.Vector(5.0, 3.0)


            if 'jump' in self.accels and self.accels['jump'] != 0:
                self.accels['jump'] -= 10
            elif self.currState == "JNORM":
                self.currState = "IDLE"

        elif self.currState == "JUMP_NEUTRAL":
            self.jumping = True
            self.accels['jump'] = 200.0
            self.targetVelocities['jump'] = actor.vector.Vector(None, 4.0)
            self.currState = "JUMP_NEUTRAL"

        elif self.currState == "IDLE":
            self.accels['move'] = 20.0
            self.targetVelocities['move'] = actor.vector.Vector(0.0, None)
            if 'jump' in self.accels:
                self.accels.pop('jump')
                self.targetVelocities.pop('jump')
'''






