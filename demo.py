import pygame
import os
import actor
import playerActor
import gearActor
import vector
import physicsManager
import animation
from pygame.locals import *
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 480, 640
        # Need a clock to scale physics vectors
        self.clock = pygame.time.Clock()
        # Keep a group of renderable actors
        self.renderables = pygame.sprite.LayeredUpdates()
        # Keep a group of gear colliders
        self.gears = pygame.sprite.Group()
        # Temporary background
        self.background = pygame.Surface((480, 640))
        self.background.fill((0, 0, 0))
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.SWSURFACE)
        self._running = True
        # create actors
        # 0: player actor. uses gravity, part of renderables
        # 1: static actor. doesn't use gravity, part of renderables and staticColliders
        playerInfo = {"IDLE" : (0, 4)}
        #playerAnimation = animation.Animation(os.path.join('Art', 'idleRight.png'), pygame.Rect(0, 0, 96, 144), playerInfo)
        #playerAnimation.update_frame("IDLE")

        #=========

        #self.playerA = playerActor.PlayerActor(vector.Vector(0,0), playerAnimation, (self.renderables))
        
        gearInfo = {"SINGLEFRAME" : (0, 1)}
        gearAnimation = animation.Animation(os.path.join('Art', 'verticalGear1.png'), pygame.Rect(0, 0, 48, 48), gearInfo)
        gearAnimation.update_frame("SINGLEFRAME")
        gearA = gearActor.GearActor(vector.Vector(0, 500), gearAnimation, False, (self.renderables, self.gears))

        self.actors = (self.playerA, gearA)
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        # update at 60 fps
        self.clock.tick(60)
        # update inputs
        self.playerA.update()
        print(self.playerA.velocity)
        # spin gears
        for gear in self.gears.sprites():
            gear.rotateGear()
        # update physics for each actor in the game
        for a in self.actors:
            a.updatePhysics(self.clock.get_time())
        # check for collisions with player against gears group
        collisionList = physicsManager.checkCollisionAgainstGroup(self.playerA, self.gears)
        # if there were collisions with player, resolve intersections
        for collider in collisionList.keys():
            physicsManager.resolveIntersection(self.playerA, collider)

    def on_render(self):
        # Draw everything in the LayeredUpdates group
        dirty = self.renderables.draw(self._display_surf)
        # Update the window
        pygame.display.update(dirty)
        # Clear the previously rendered stuff
        self.renderables.clear(self._display_surf, self.background)
   
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def load_player_sprites(self):
        PLAYERSIZE = pygame.Rect(0, 0, 96, 144)
        info_dic = {"idleLeft": (0, 4),
                    "idleRight": (1, 4),
                    "moveLeft": (2, 4),
                    "moveRight": (3, 4),
                    "turnToLeft": (4, 7),
                    "turnToRight": (5, 7)}
        self.playerAnimation = animation.Animation(os.path.join('Art', 'playerSheet.png'),
                                                   PLAYERSIZE,
                                                   info_dic)

    def load_death_sprites(self):
        DEATHSIZE = pygame.Rect(0, 0, 240, 240)
        info_dic = {"deathLeft": (0, 9),
                    "deathRight": (1, 9)}
        self.deathAnimation = animation.Animation(os.path.join('Art', 'deathSheet'),
                                                    DEATHSIZE,
                                                    info_dic)

    def load_gear_sprites(self):
        GEARSIZE1 = pygame.Rect(0, 0, 48, 48)
        GEARSIZE2 = pygame.Rect(0, 0, 96, 96)
        GEARSIZE3 = pygame.Rect(0, 0, 144, 144)
        info_dic1 = {"sVertGear": (0, 1)}
        info_dic2 = {"mVertGear": (0, 1)}
        info_dic3 = {"lVertGear": (0, 1)}

        self.sVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear1'),
                                                        GEARSIZE1,
                                                        info_dic1)
        self.mVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear2'),
                                                        GEARSIZE2,
                                                        info_dic2)
        self.lVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear3'),
                                                        GEARSIZE3,
                                                        info_dic3)








 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
