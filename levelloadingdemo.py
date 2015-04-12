import playerActor
import gearActor
import vector
import physicsManager
import animation
from pygame.locals import *
import tile_loader
import sprites
import os
import pygame
import random 

SCREEN_X_NS = 528 #screen width w/o sidebar
SCREEN_X = 728 #screen width w/ sidebar
SCREEN_Y = 720
BOX_SIZE = 48
H_BOXES =  11
V_BOXES =  15
LEVEL_LIST = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt','level5.txt', 
'level6.txt', 'level7.txt','level8.txt','level9.txt','level10.txt','level11.txt',
'level12.txt','level13.txt','level.14txt','level15.txt','level16.txt','level17.txt',
'level18.txt']

def draw_grid(surface):
	 for i in range(1,H_BOXES):
		  pygame.draw.line(surface, pygame.Color(255,255,255,255), (i*BOX_SIZE,0),(i*BOX_SIZE,SCREEN_Y))
	 for i in range(1,V_BOXES):
		  pygame.draw.line(surface, pygame.Color(255,255,255,255),(0,i*BOX_SIZE),(SCREEN_X_NS,i*BOX_SIZE))
	 pygame.display.update()

def open_matrix(path):
	if path == ".":
		pass
	else:
		matrix = []
		file_matrix = [line.rstrip() for line in open(path, 'r')]
		for row in file_matrix:
			matrix.append(list(row))
	return matrix

class Main:
	def __init__(self):
		self._running = True
		self.box_size = 48
		self.size = (self.weight, self.height) = (528, 720)
		self.clock = pygame.time.Clock()
		self.renderables = pygame.sprite.LayeredUpdates()
		self.gears = pygame.sprite.Group()

	def on_init(self):
		pygame.init()
		self.window = pygame.display.set_mode(self.size, pygame.SRCALPHA)
		self._running = True
		self.player = self.get_player_actor(0,0,-20)
	
	
	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
	
	def on_loop(self):
		# update at 60 fps
		self.clock.tick(60)
		# update inputs
		#self.player.update()
		# spin gears
		for gear in self.gears.sprites():
			gear.rotateGear()
		# update physics for each actor in the game
		#for a in self.actors:
		#	a.updatePhysics(self.clock.get_time())
		# check for collisions with player against gears group
		collisionList = physicsManager.checkCollisionAgainstGroup(self.player, self.gears)
		# if there were collisions with player, resolve intersections
		for collider in collisionList.keys():
			physicsManager.resolveIntersection(self.player, collider)
	
	def on_render(self):
		dirty = self.renderables.draw(self.window)
		pygame.display.update(dirty)
		self.renderables.clear(self.window, sprites.SpriteList[2])

	def on_execute(self):
		if self.on_init() == False:
			self._running == False
		self.load_level(open_matrix(os.path.realpath(self.random_level())), sprites.SpriteList[2])
		while(self._running):
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
		self.on_cleanup()

	def on_cleanup(self):
		pygame.quit()

	def random_level(self):
		random_item = random.choice(LEVEL_LIST)
		return str(random_item)

	def load_level(self, level_matrix, background):
		backgroundRect = background.get_rect()
		self.window.blit(background, backgroundRect)
		print(level_matrix)
		for i in level_matrix:
			for x in range(len(i)):
				self.get_object(level_matrix.index(i),x, i[x])

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
				self.get_sVertGearActor(start_x, start_y, False)
			elif element == "w":
				self.get_mVertGearActor(start_x, start_y, False)
			elif element == "e":
				self.get_lVertGearActor(start_x-48, start_y-48, False)
			elif element == "x":
				return None
			elif element == "f":
				return None
			elif element == "r":
				return None
		else:
			if element == "Q":
				self.get_sVertGearActor(start_x, start_y, True)
			elif element == "W":
				self.get_mVertGearActor(start_x, start_y, True)
			elif element == "E":
				self.get_lVertGearActor(start_x-48, start_y-48, True)
			elif element == "X":
				return None
			elif element == "F":
				return None
			elif element == "R":
				return None


			
	def get_lVertGearActor(self, x, y, clockwise):
		"""
		:return: gearActor, function creates a large gear and puts it in the ONLY state. Rotation is done in code.
		"""
		GEARSIZE3 = pygame.Rect(x, y, 144, 144)
		info_dic3 = {"lVertGear": (0, 1)}
		lVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear3.png'),
																		  GEARSIZE3,
																		  info_dic3)
		lVertGearAnimation.update_frame("lVertGear")
		gearActor.GearActor(vector.Vector(x, y), lVertGearAnimation, clockwise, (self.renderables, self.gears))

	def get_mVertGearActor(self, x, y, clockwise):
		"""
		:return: gearActor, function creates a medium gear and puts it in the ONLY state. Rotation is done in code.
		"""
		GEARSIZE2 = pygame.Rect(x, y, 96, 96)
		info_dic2 = {"mVertGear": (0, 1)}
		mVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear2.png'), GEARSIZE2, info_dic2)
		mVertGearAnimation.update_frame("mVertGear")
		gearActor.GearActor(vector.Vector(x, y), mVertGearAnimation, clockwise, (self.renderables, self.gears))

	def get_sVertGearActor(self, x, y, clockwise):
		"""
		:return: gearActor, function creates a small gear and puts it in the ONLY state. Rotation is done in code.
		"""
		GEARSIZE1 = pygame.Rect(x, y, 48, 48)
		info_dic1 = {"sVertGear": (0, 1)}
		sVertGearAnimation = animation.Animation(os.path.join('Art', 'verticalGear1.png'), GEARSIZE1, info_dic1)
		sVertGearAnimation.update_frame("sVertGear")
		gearActor.GearActor(vector.Vector(x, y), sVertGearAnimation, clockwise, (self.renderables, self.gears))

	def get_spawn(self, x, y):
		"""
		:return: spawnTrigger, function creates a spawn point, where the player spawns:
		"""
		return 


while __name__ == "__main__":
	game = Main()
	game.on_execute()
