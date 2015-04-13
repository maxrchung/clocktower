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
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.SWSURFACE)
        self._running = True
        # create actors
        # 0: player actor. uses gravity, part of renderables
        # 1: static actor. doesn't use gravity, part of renderables and staticColliders
        #playerInfo = {"IDLE" : (0, 4)}
        #playerAnimation = animation.Animation(os.path.join('Art', 'idleRight.png'), pygame.Rect(0, 0, 96, 144), playerInfo)
        #playerAnimation.update_frame("IDLE")
        # load all sprites
        #self.load_player_sprites()
        #self.load_death_sprites()
        #self.load_gear_sprites()
        #self.playerAnimation.update_frame("idleLeft")
        #gearInfo = {"SINGLEFRAME" : (0, 1)}
        #gearAnimation = animation.Animation(os.path.join('Art', 'verticalGear1.png'), pygame.Rect(0, 0, 48, 48), gearInfo)
        self.background = pygame.image.load(os.path.join('Art', 'background.png')).convert_alpha()
        
        self.player = self.get_player_actor(0, 0, -30)
        gearA = self.get_sVertGearActor(0, 500, False)
        gearB = self.get_mVertGearActor(30, 400, True)
        gearC = self.get_lVertGearActor(200, 300, False)
        
        self.actors = (gearA, gearB, gearC, self.player)
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        # update at 60 fps
        self.clock.tick(60)
        # update inputs
        self.player.update()
        # spin gears
        for gear in self.gears.sprites():
            gear.rotateGear()
        # update physics for each actor in the game
        for a in self.actors:
            a.updatePhysics(self.clock.get_time())
        # check for collisions with player against gears group
        collisionList = physicsManager.checkCollisionAgainstGroup(self.player, self.gears)
        if collisionList:
            self.player.jumping = False
            # if there were collisions with player, resolve intersections
            physicsManager.resolveIntersection(self.player, collisionList)

    def on_render(self):
        # Draw everything in the LayeredUpdates group
        #dirty = self.renderables.draw(self._display_surf)
        # Update the window
        #pygame.display.update(dirty)
        # Clear the previously rendered stuff
        #self.renderables.clear(self._display_surf, self.background)
        self._display_surf.blit(self.background, (0,0))
        for a in self.actors:
            self._display_surf.blit(a.image, (a.pos.x, a.pos.y))
        pygame.display.update()
   
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

    def get_player_actor(self, x, y, scale):
        PLAYERSIZE = pygame.Rect(0, 0, 96, 144)
        info_dic = {"idleLeft": (0, 4),
                    "idleRight": (1, 4),
                    "moveLeft": (2, 4),
                    "moveRight": (3, 4),
                    "turnToLeft": (4, 7),
                    "turnToRight": (5, 7)}
        playerAnimation = animation.Animation(os.path.join('Art', 'playerSheet.png'),
                                                   PLAYERSIZE,
                                                   info_dic, scale)
        playerAnimation.update_frame("idleRight")
        return playerActor.PlayerActor(vector.Vector(x, y), playerAnimation, 40, (self.renderables))

    def get_death_actor(self, x, y, scale):
        """
        :return: actor, function creates a death animation and puts it at the given x and y
        """
        DEATHSIZE = pygame.Rect(0, 0, 240, 240)
        info_dic = {"deathLeft": (0, 9),
                    "deathRight": (1, 9)}
        deathAnimation = animation.Animation(os.path.join('Art', 'deathSheet.png'),
                                                    DEATHSIZE,
                                                    info_dic,
                                                    scale)
        deathAnimation.update_frame("deathLeft")
        return actor.Actor(vector.Vector(x, y), deathAnimation, False, 40, (self.renderables))

    def get_lVertGearActor(self, x, y, clockwise):
        """
        :return: gearActor, function creates a large gear and puts it in the ONLY state. Rotation is done in code.
        """
        GEARSIZE3 = pygame.Rect(0, 0, 144, 144)
        info_dic3 = {"lVertGear": (0, 1)}
        lVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear3.png'),
                                                        GEARSIZE3,
                                                        info_dic3)
        lVertGearAnimation.update_frame("lVertGear")
        return gearActor.GearActor(vector.Vector(x, y), lVertGearAnimation, clockwise, 60, (self.renderables, self.gears))

    def get_mVertGearActor(self, x, y, clockwise):
        """
        :return: gearActor, function creates a medium gear and puts it in the ONLY state. Rotation is done in code.
        """
        GEARSIZE2 = pygame.Rect(0, 0, 96, 96)
        info_dic2 = {"mVertGear": (0, 1)}
        mVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear2.png'),
                                                        GEARSIZE2,
                                                        info_dic2)
        mVertGearAnimation.update_frame("mVertGear")
        return gearActor.GearActor(vector.Vector(x, y), mVertGearAnimation, clockwise, 45, (self.renderables, self.gears))

    def get_sVertGearActor(self, x, y, clockwise):
        """
        :return: gearActor, function creates a small gear and puts it in the ONLY state. Rotation is done in code.
        """
        GEARSIZE1 = pygame.Rect(0, 0, 48, 48)
        info_dic1 = {"sVertGear": (0, 1)}
        sVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear1.png'),
                                                        GEARSIZE1,
                                                        info_dic1)
        sVertGearAnimation.update_frame("sVertGear")
        return gearActor.GearActor(vector.Vector(x, y), sVertGearAnimation, clockwise, 24, (self.renderables, self.gears))









 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
