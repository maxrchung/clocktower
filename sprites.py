import pygame
import actor
import gearActor
import tile_loader


v_gear = pygame.image.load(os.path.join('Art','verticalGear1.png'))
v_gear_med = pygame.image.load(os.path.join('Art', 'verticalGear2.png'))
v_gear_big = pygame.image.load(os.path.join('Art', 'verticalGear3.png'))
start_tile = pygame.image.load(os.path.join('Art', 'ladderBottom.png'))
end_tile = pygame.image.load(os.path.join('Art', 'ladderTop.png'))
background = pygame.image.load(os.path.join('Art', 'background.png'))

#Sprite List
#Start_tile = 0
#End_tile = 1
#v_gear1by1 = 2
#v_gear_med2by2 = 3
#v_gear_big3by3 = 4
#background = 5

SpriteList = [start_tile, end_tile, background, v_gear, v_gear_med, v_gear_big]

class Gear_Sprites(pygame.sprite.Sprite):
	def __init__(self, x, y, matrix):
		self.SpriteList = []

