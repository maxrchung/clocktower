import pygame
import os
import actor
import playerActor
import gearActor
import vector
import physicsManager
import animation
from pygame.locals import *
import os
import pygame
import random
import tile_loader
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 728, 720
        self.H_BOXES = 11
        self.V_BOXES = 15
        self.box_size = 48
        self.LEVEL_LIST = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt','level5.txt', 
'level6.txt', 'level7.txt','level8.txt','level9.txt','level10.txt','level11.txt',
'level12.txt','level13.txt','level.14txt','level15.txt','level16.txt','level17.txt',
'level18.txt']
        # Need a clock to scale physics vectors
        self.clock = pygame.time.Clock()
        # Keep a group of renderable actors
        self.renderables = pygame.sprite.LayeredUpdates()
        # Keep a group of gear colliders
        self.gears = pygame.sprite.Group()
    
    def draw_grid(surface):
        for i in range(1,H_BOXES):
            pygame.draw.line(surface, pygame.Color(255,255,255,255), (i*BOX_SIZE,0),(i*BOX_SIZE,SCREEN_Y))
        for i in range(1,V_BOXES):
            pygame.draw.line(surface, pygame.Color(255,255,255,255),(0,i*BOX_SIZE),(SCREEN_X_NS,i*BOX_SIZE))
    
        pygame.display.update()

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
        #self.load_death_sprites()leve
        #self.load_gear_sprites()
        #self.playerAnimation.update_frame("idleLeft")
        #gearInfo = {"SINGLEFRAME" : (0, 1)}
        #gearAnimation = animation.Animation(os.path.join('Art', 'verticalGear1.png'), pygame.Rect(0, 0, 48, 48), gearInfo)
        self.background = pygame.image.load(os.path.join('Art', 'background.png')).convert_alpha()
        self.clocktowertear = pygame.image.load(os.path.join('Art', 'clocktowertear.png')).convert_alpha()
        self.clocktower = pygame.image.load(os.path.join('Art', 'clocktower.png')).convert_alpha()
        self.player = self.get_player_actor(0,0,-20)
        self.actors = []
 
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
        for collider, point in collisionList.items():
            physicsManager.resolveIntersection(self.player, collider)

    def on_render(self):
        # Draw everything in the LayeredUpdates group
        #dirty = self.renderables.draw(self._display_surf)
        # Update the window
        #pygame.display.update(dirty)
        # Clear the previously rendered stuff
        #self.renderables.clear(self._display_surf, self.background)
        self._display_surf.blit(self.background, (0,0))
        self._display_surf.blit(self.clocktowertear,(720-247,0))
        self._display_surf.blit(self.clocktower,(528,0))
        for a in self.actors:
            if a.tear:
                self._display_surf.blit(a.tear, (a.tearpos[0], a.tearpos[1]))
            self._display_surf.blit(a.image, (a.pos.x, a.pos.y))
        pygame.display.update()
   
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        self.load_level(self.open_matrix(os.path.realpath('level1.txt')))
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def random_level(self):
        random_item = random.choice(self.LEVEL_LIST)
        return str(random_item)

    def load_level(self, level_matrix):
        print(level_matrix)
        for i in level_matrix:
            for x in range(len(i)):
                actor = self.get_object(level_matrix.index(i),x, i[x])
                if actor == None:
                    pass
                else:
                    self.actors.append(actor)
   
    def open_matrix(self, path):
        if path == ".":
            pass
        else:
            matrix = []
            file_matrix = [line.rstrip() for line in open(path, 'r')]
            for row in file_matrix:
                matrix.append(list(row))
        return matrix
    
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
        return playerActor.PlayerActor(vector.Vector(x, y), playerAnimation, (self.renderables))
    

    def get_object(self, row, col, element):
        start_x = col * self.box_size
        start_y = row * self.box_size

        if element.islower():
            if element == "q":
                return self.get_sVertGearActor(start_x, start_y, False)
            elif element == "w":
                return self.get_mVertGearActor(start_x, start_y, False)
            elif element == "e":
                return self.get_lVertGearActor(start_x-48, start_y-48, False)
            elif element == "x":
                pass
            elif element == "f":
                pass
                #self.get_player_actor(start_x, start_y, -20)
            elif element == "r":
                pass
        else:
            if element == "Q":
                return self.get_sVertGearActor(start_x, start_y, True)
            elif element == "W":
                return self.get_mVertGearActor(start_x, start_y, True)
            elif element == "E":
                return self.get_lVertGearActor(start_x-48, start_y-48, True)
            elif element == "X":
                pass
            elif element == "F":
                pass
                #self.get_player_actor(start_x, start_y, -20)
            elif element == "R":
                pass
        pass
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
        return actor.Actor(vector.Vector(x, y), deathAnimation, False, (self.renderables))

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
        return gearActor.GearActor(vector.Vector(x, y), lVertGearAnimation, clockwise, (self.renderables, self.gears), id="LARGE")

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
        return gearActor.GearActor(vector.Vector(x, y), mVertGearAnimation, clockwise, (self.renderables, self.gears), id="MEDIUM")

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
        return gearActor.GearActor(vector.Vector(x, y), sVertGearAnimation, clockwise, (self.renderables, self.gears), id="SMALL")









 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
