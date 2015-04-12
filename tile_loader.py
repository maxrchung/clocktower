import pygame
import sprites
import actor
import gearActor

Spirtes = Sprites.sprites
class Level:
	def __init__(self, screen, tiles, sprites):
		"""Initializes a game window, and a tile matrix"""
		self.window = screen
		self.matrix = tiles
		self.spritelist = sprites

	def parser(self):
		#Sprite List
		#Start_tile = 0
		#End_tile = 1
		#v_gear1by1 = 2
		#v_gear_med2by2 = 3
		#v_gear_big3by3 = 4
		#background = 5
		"""Parses through the data and passes to appropriate draw function"""
		self.window.blit(self.spritelist[5])
		for row in self.matrix:
			for col in row:
				if col.islower():
					self.draw_counterclockwise(col)
				else:
					self.draw_clockwise(col)

	def draw_clockwise(self, element):
		"""Draws the counter clockwise element onto the game screen"""
		if element == "Q":
			self.spritelist[2]
		elif element == "W":
			self.spritelist[3]
		elif element == "E":
			self.spritelist[4]
	def draw_counterclockwise(self, element):
		"""Draws the clockwise element onto the game screen"""
		if element == "X":
			pass
		elif element == "Q":
			pass