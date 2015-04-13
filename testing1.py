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
import soundManager
import clockTower
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 720, 720
        self.H_BOXES = 11
        self.V_BOXES = 15
        self.box_size = 48
        self.LEVEL_LIST = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt','level5.txt', 
'level6.txt', 'level7.txt','level8.txt','level9.txt','level10.txt','level11.txt',
'level12.txt','level13.txt','level14.txt','level15.txt','level16.txt','level17.txt',
'level18.txt']
        self.game_state = "START"
        self.game_load = True
        self.game_counter = 0
        # Need a clock to scale physics vectors
        self.clock = pygame.time.Clock()
        # Keep a group of renderable actors
        self.renderables = pygame.sprite.LayeredUpdates()
        # Keep a group of gear colliders
        self.gears = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.ladders1 = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        # Playing Sound Effects
        self.sound = soundManager.SoundManager()
        self.sound.playMusic("Tower Climb.mp3", -1)
        self.sound.setVolume(0.25)
    
    def draw_grid(surface):
        for i in range(1,H_BOXES):
            pygame.draw.line(surface, pygame.Color(255,255,255,255), (i*BOX_SIZE,0),(i*BOX_SIZE,SCREEN_Y))
        for i in range(1,V_BOXES):
            pygame.draw.line(surface, pygame.Color(255,255,255,255),(0,i*BOX_SIZE),(SCREEN_X_NS,i*BOX_SIZE))
    
        pygame.display.update()

    def on_init(self):
        pygame.init()
        icon = pygame.image.load('Art/iloveit.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Minutes to Midnight")
        self._display_surf = pygame.display.set_mode(self.size, pygame.SRCALPHA)
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
        self.clocktower_tear = pygame.image.load(os.path.join('Art', 'clockTowerTear.png')).convert_alpha()
        self.start = pygame.image.load(os.path.join('Art', 'start.png')).convert_alpha()
        self.win = pygame.image.load(os.path.join('Art', 'win.png')).convert_alpha()
        self.lose = pygame.image.load(os.path.join('Art', 'lose.png')).convert_alpha()
        self.player_marker = pygame.image.load(os.path.join('Art', 'playerMarker.png')).convert_alpha()
        self.minute_hand = clockTower.Hand(self._display_surf)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if self.game_state == "START" or self.game_state == "WIN" or self.game_state == "LOSE":
                if event.key == pygame.K_RETURN:
                    return True
    
    def on_loop(self):
        # update at 60 fps
        self.clock.tick(60)
        if self.game_state == "START":
            pass
        elif self.game_state == "GAME":    
            if self.game_load:
                self.player = self.get_player_actor(240,540,-30)
                self.actors = [self.player, self.get_wall(0,0, False), self.get_wall(0,0, True), self.get_wall(528,0, True)]
                self.level_name = "test.txt"#self.random_level()
                print(self.level_name)
                self.game_counter += 1
                print(self.game_counter)
                self.load_level(self.open_matrix(os.path.realpath(self.level_name)))
                self.game_load = False
            # update inputs
            self.player.update()
            self.minute_hand.update()
            # spin gears
            for gear in self.gears.sprites():
                gear.rotateGear()
            # update physics for each actor in the game
            for a in self.actors:
                a.updatePhysics(self.clock.get_time())
            # check for collisions with player against gears group
            collisionList = physicsManager.checkCollisionAgainstGroup(self.player, self.gears)
            # move player if he's touching a gear
            if collisionList:
                self.player.accels['gear'] = 10.0
                for gearCollide in collisionList:
                    # CLOCKWISE
                    if gearCollide.clockwise:
                        if self.player.rect.centery < gearCollide.rect.centery:
                            if self.player.rect.centerx < gearCollide.rect.centerx:
                                # TOPLEFT
                                self.player.targetVelocities['gear'] = vector.Vector(1.0, 2.0).get_norm()
                            else:
                                # TOPRIGHT
                                self.player.targetVelocities['gear'] = vector.Vector(1.0, -1.0).get_norm()
                        else:
                            if self.player.rect.centerx < gearCollide.rect.centerx:
                                # BOTTOMLEFT
                                self.player.targetVelocities['gear'] = vector.Vector(-1.0, 2.0).get_norm()
                            else:
                                # BOTTOMRIGHT
                                self.player.targetVelocities['gear'] = vector.Vector(-1.0, -1.0).get_norm()
                    # COUNTERCLOCKWISE
                    else:
                        if self.player.rect.centery < gearCollide.rect.centery:
                            if self.player.rect.centerx < gearCollide.rect.centerx:
                                # TOPLEFT
                                self.player.targetVelocities['gear'] = vector.Vector(-1.0, -1.0).get_norm()
                            else:
                                # TOPRIGHT
                                self.player.targetVelocities['gear'] = vector.Vector(-1.0, 2.0).get_norm()
                        else:
                            if self.player.rect.centerx < gearCollide.rect.centerx:
                                # BOTTOMLEFT
                                self.player.targetVelocities['gear'] = vector.Vector(1.0, -1.0).get_norm()
                            else:
                                # BOTTOMRIGHT
                                self.player.targetVelocities['gear'] = vector.Vector(1.0, 2.0).get_norm()
            else:
                self.player.accels['gear'] = 0.0
                self.player.targetVelocities['gear'] = vector.Vector(None, None)
            # check more collisions
            collisionList.extend(physicsManager.checkCollisionAgainstGroup(self.player, self.ladders))
            collisionList.extend(physicsManager.checkCollisionAgainstGroup(self.player, self.ladders1))
            collisionNextLevel = physicsManager.checkCollisionAgainstGroup(self.player, self.ladders)
            collisionDeath = physicsManager.checkCollisionAgainstGroup(self.player, self.walls)
			# if a player's standing on something, reset jump
            if collisionList:
                for collider in collisionList:
                    if self.player.rect.centery < collider.rect.centery:
                        self.player.jumping = False
                        self.player.accels['gravity'] = 0.0
                        self.player.velocity.y = 0.0
                # if there were collisions with player, resolve intersections
                physicsManager.resolveIntersection(self.player, collisionList)
            else:
                self.player.accels['gravity'] = 4.0
            # prevent player from leaving top left bottom
            if self.player.rect.x < 0:
                self.player.moveActor(-1*self.player.rect.x, 0)
            if self.player.rect.y < 0:
                self.player.moveActor(0, -1*self.player.rect.y)
            if self.player.rect.x > 480:
                self.player.moveActor(480 - self.player.rect.x, 0)
            if self.player.rect.bottom > self.height:
                collisionDeath = True
                #deathActor = self.get_death_actor(self.player.pos.x, self.player.pos.y, -30)
                #self.loop_death(deathActor)
            # check if the player got to the top ladder
            if collisionNextLevel:
                self.game_load = True
            if collisionDeath:
                self.game_state = "LOSE"
            # if there were collisions with player, resolve intersections

                

    def on_render(self):
        # Draw everything in the LayeredUpdates group
        #dirty = self.renderables.draw(self._display_surf)
        # Update the window
        #pygame.display.update(dirty)
        # Clear the previously rendered stuff
        #self.renderables.clear(self._display_surf, self.background)
        if self.game_counter > 6:
            self.game_state = "WIN"
        if self.game_state == "START":
            self._display_surf.blit(self.background, (0,0))
            self._display_surf.blit(self.start,(0,0))
            self._display_surf.blit(self.clocktowertear, (720-247,0))
            self._display_surf.blit(self.clocktower,(528,0))
            self._display_surf.blit(self.clocktower,(528,0))
        elif self.game_state == "GAME":
            self._display_surf.blit(self.background, (0,0))
            self._display_surf.blit(self.clocktowertear,(720-247,0))
            self._display_surf.blit(self.clocktower,(528,0))
            self._display_surf.blit(self.player_marker, (550, 720 - (100 *self.game_counter)))
            for a in self.actors:
                if a.tear:
                    self._display_surf.blit(a.tear, (a.tearpos[0], a.tearpos[1]))
                self._display_surf.blit(a.image, (a.pos.x, a.pos.y))
            self.minute_hand.draw()
        elif self.game_state == "WIN":
            #self.sound.playSoundEffect('Level Completed.wav')
            self._display_surf.blit(self.background, (0,0))
            self._display_surf.blit(self.win,(0,0,))
            self._display_surf.blit(self.clocktowertear, (720-247,0))
            self._display_surf.blit(self.clocktower,(528,0))
            self._display_surf.blit(self.player_marker, (550, 720 - (100 *self.game_counter)))
        elif self.game_state == "LOSE":
            #self.sound.playMusic('Clock Strikes Twelve.mp3', 1)
            self._display_surf.blit(self.background, (0,0))
            self._display_surf.blit(self.lose,(0,0,))
            self._display_surf.blit(self.clocktowertear, (720-247,0))
            self._display_surf.blit(self.clocktower,(528,0))
        pygame.display.update()
   
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            for event in pygame.event.get():
                if self.on_event(event):
                    self.game_state = "GAME"
                    self.game_counter = 0
                    self.game_load = True
                #print(self.game_state)
                # self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def random_level(self):
        random_item = random.choice(self.LEVEL_LIST)
        self.LEVEL_LIST.remove(random_item)
        return str(random_item)

    def load_level(self, level_matrix):
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
        return playerActor.PlayerActor(vector.Vector(x, y), playerAnimation, 48,(self.renderables))
    

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
                #self.get_player_actor(start_x, start_y, -20)
                return self.get_ladder_top_actor(start_x, start_y)
            elif element == "r":
                return self.get_ladder_bottom_actor(start_x, start_y-48)
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
                #self.get_player_actor(start_x, start_y, -20)
                return self.get_ladder_top_actor(start_x, start_y)
            elif element == "R":
                return self.get_ladder_bottom_actor(start_x, start_y-48)
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
        deathAnimation.update_frame("death" + self.player.curr_orientation)
        return actor.Actor(vector.Vector(x, y), deathAnimation, False, 120, (self.renderables))

    def loop_death(self, death_actor):
        count = 0
        for i in range(9):
            if count == 10:
                death_actor.get_current_frame()
                death_actor.update_current_frame()
                count = 0
            else:
                count += 1

    def get_lVertGearActor(self, x, y, clockwise):
        """
        :return: gearActor, function creates a large gear and puts it in the ONLY state. Rotation is done in code.
        """
        GEARSIZE3 = pygame.Rect(0, 0, 144, 144)
        info_dic3 = {"lVertGear": (0, 1)}
        if clockwise:
            lVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear3.png'),
                                                        GEARSIZE3,
                                                        info_dic3)
        else:
            lVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear3counter.png'),
                                                        GEARSIZE3,
                                                        info_dic3)
        lVertGearAnimation.update_frame("lVertGear")
        return gearActor.GearActor(vector.Vector(x, y), lVertGearAnimation, clockwise, 72, (self.renderables, self.gears), id="LARGE")

    def get_mVertGearActor(self, x, y, clockwise):
        """
        :return: gearActor, function creates a medium gear and puts it in the ONLY state. Rotation is done in code.
        """
        GEARSIZE2 = pygame.Rect(0, 0, 96, 96)
        info_dic2 = {"mVertGear": (0, 1)}
        if clockwise:
            mVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear2.png'),
                                                        GEARSIZE2,
                                                        info_dic2)
        else:
            mVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear2counter.png'),
                                                        GEARSIZE2,
                                                        info_dic2)
        mVertGearAnimation.update_frame("mVertGear")
        return gearActor.GearActor(vector.Vector(x, y), mVertGearAnimation, clockwise, 48, (self.renderables, self.gears), id="MEDIUM")

    def get_sVertGearActor(self, x, y, clockwise):
        """
        :return: gearActor, function creates a small gear and puts it in the ONLY state. Rotation is done in code.
        """
        GEARSIZE1 = pygame.Rect(0, 0, 48, 48)
        info_dic1 = {"sVertGear": (0, 1)}
        if clockwise:
            sVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear1.png'),
                                                        GEARSIZE1,
                                                        info_dic1)
        else:
            sVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear1counter.png'),
                                                        GEARSIZE1,
                                                        info_dic1)
        sVertGearAnimation.update_frame("sVertGear")
        return gearActor.GearActor(vector.Vector(x, y), sVertGearAnimation, clockwise, 24, (self.renderables, self.gears), id="SMALL")

    def get_ladder_bottom_actor(self, x, y):
        """
        :return: a ladder actor
        """
        LADDERSIZE = pygame.Rect(0, 0, 48, 96)
        info_dic1 = {"sVertGear": (0, 1)}
        sVertGearAnimation = animation.Animation(os.path.join('Art', 'ladderBottom.png'),
                                                        LADDERSIZE,
                                                        info_dic1)
        sVertGearAnimation.update_frame("sVertGear")
        return actor.Actor(vector.Vector(x, y), sVertGearAnimation, False, 48, (self.renderables, self.ladders1), id="LADDER_BOTTOM")

    def get_ladder_top_actor(self, x, y):
        """
        :return: a ladder actor
        """
        LADDERSIZE = pygame.Rect(0, 0, 48, 96)
        info_dic1 = {"sVertGear": (0, 1)}
        sVertGearAnimation = animation.Animation(os.path.join('Art', 'ladderTop.png'),
                                                        LADDERSIZE,
                                                        info_dic1)
        sVertGearAnimation.update_frame("sVertGear")
        return actor.Actor(vector.Vector(x, y), sVertGearAnimation, False, 48, (self.renderables, self.ladders), id="LADDER_TOP")

    def get_wall(self, x,y, type):
        """
        :return: a wall
        """

        if type:
            LADDERSIZE = pygame.Rect(0, 0, 48, 48)
            info_dic1 = {"sVertGear": (0, 1)}
            sVertGearAnimation = animation.Animation(os.path.join('Art', 'wallLeftRight.png'),
                                                        LADDERSIZE,
                                                        info_dic1)
        else:
            LADDERSIZE = pygame.Rect(0, 0, 48, 48)
            info_dic1 = {"sVertGear": (0, 1)}
        sVertGearAnimation = animation.Animation(os.path.join('Art', 'wallTopBottom.png'),
                                                        LADDERSIZE,
                                                        info_dic1)
        sVertGearAnimation.update_frame("sVertGear")
        return actor.Actor(vector.Vector(x, y), sVertGearAnimation, False, 1, (self.renderables, self.walls))








 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
