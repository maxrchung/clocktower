import pygame
import os
import tile_matrix
import easygui
from pygame import gfxdraw

# Module Documentation
# Pygame - Main display engine
# os - Used to load images
# tile_matrix - Matrix module creating .txt output of level layout
# easygui - File browser dialogue

pygame.display.init()
pygame.display.set_caption('Tile Editor')
SCREEN_X_NS = 528
SCREEN_X = 728
SCREEN_Y = 720
V_BOXES = 15
H_BOXES = 11
BOX_SIZE = 48

v_gear = pygame.image.load(os.path.join('Art','tile_v_gear1by1.png'))
v_gear_med = pygame.image.load(os.path.join('Art', 'tile_v_gear3by3.png'))
v_gear_big = pygame.image.load(os.path.join('Art', 'tile_v_gear5by5.png'))
h_gear = pygame.image.load(os.path.join('Art', 'tile_h_gear1by1.png'))
h_gear_med = pygame.image.load(os.path.join('Art', 'tile_h_gear1by3.png'))
h_gear_big = pygame.image.load(os.path.join('Art', 'tile_h_gear1by5.png'))
start_tile = pygame.image.load(os.path.join('Art', 'tile_start1by1.png'))
end_tile = pygame.image.load(os.path.join('Art', 'tile_end1by1.png'))
side_bar = pygame.image.load(os.path.join('Art', 'side_bar.png'))
background = pygame.image.load(os.path.join('Art', 'foreground.png'))

backgroundRect = background.get_rect()
main_window = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
background_window = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
background_window.blit(background, backgroundRect)
main_window.blit(side_bar, pygame.Rect(SCREEN_X_NS, 0 , 200, SCREEN_Y))

tm = tile_matrix.Tile_Matrix(H_BOXES, V_BOXES)
tm.change_matrix(0, 5, "F")
tm.change_matrix(1, 5, "F")
pygame.display.update()
black = pygame.Color(0,0,0)

is_running = True

def draw_grid(surface):
	"""Draws the Grid"""
	for i in range(1,H_BOXES):
		pygame.draw.line(surface, pygame.Color(255,255,255,255), (i*BOX_SIZE,0),(i*BOX_SIZE,SCREEN_Y))
	for i in range(1,V_BOXES):
  		pygame.draw.line(surface, pygame.Color(255,255,255,255),(0,i*BOX_SIZE),(SCREEN_X_NS,i*BOX_SIZE))
  	pygame.display.update()

def draw_matrix(surface, matrix):
	"""Draws an opened matrix(level)"""
	for row in matrix:
		for col in row:
			if col == 

draw_grid(main_window)
current_mode = "Q" 

# Current Mode Guide
# Q = Standard v_gear
# W = Medium v_gear_med
# E = Big v_gear_big
# R = Spawn start_tile
# A = Standard h_gear
# S = Medium h_gear_med
# D = Big h_gear_med
# F = Victory end_tile

while(is_running):
    #get mouse click
    #find out which box it's in
    #draw rectangle in the box that's correct color
    #change matrix accordingly
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                current_mode = "Q"
                print(current_mode)
            elif event.key == pygame.K_w:
                current_mode = "W"
                print(current_mode)
            elif event.key == pygame.K_e:
                current_mode = "E"
                print(current_mode)
            elif event.key == pygame.K_r:
                current_mode = "R"
                print(current_mode)
            elif event.key == pygame.K_a:
                current_mode = "A"
                print(current_mode)
            elif event.key == pygame.K_s:
                current_mode = "S"
                print(current_mode)
            elif event.key == pygame.K_d:
                current_mode = "D"
                print(current_mode)
            elif event.key == pygame.K_f:
                current_mode = "F"
                print(current_mode)
            elif event.key == pygame.K_z:
                current_mode = "X"
                print(current_mode)
            elif event.key == pygame.K_x:
                path = easygui.fileopenbox()
                tm.open_matrix(path)
                main_window.blit(background, (0,0))
                draw_grid(main_window)
                draw_matrix(main_window, tm.matrix)
                pygame.display.update()
            elif event.key == pygame.K_c:
                tm.save()
            elif event.key == pygame.K_v:
                pygame.display.quit()
            elif event.key == pygame.K_SPACE:
            	tm.clear_matrix()
            	main_window.blit(background, (0,0))
            	draw_grid(main_window)
            	pygame.display.update()
            elif event.key == pygame.K_1:
            	path = easygui.fileopenbox()
            	background = pygame.image.load(path)
            	backgroundRect = background.get_rect()
            	background_window.blit(background, backgroundRect)

        if pygame.mouse.get_pos()[0] <= SCREEN_X_NS:
            if pygame.mouse.get_pressed()[0]:
                box_x = pygame.mouse.get_pos()[0] // BOX_SIZE
                box_y = pygame.mouse.get_pos()[1] // BOX_SIZE
                start_x = box_x * BOX_SIZE
                start_y = box_y * BOX_SIZE

            	print(box_x,BOX_SIZE,box_y,BOX_SIZE)
                tm.change_matrix(box_y, box_x, current_mode)
                print(box_x + 1, box_y+1)
                if current_mode == "Q":
                    main_window.blit(v_gear,pygame.Rect(start_x, start_y, BOX_SIZE, BOX_SIZE))
                if current_mode == "W":
                   main_window.blit(v_gear_med,pygame.Rect(start_x-48, start_y-48, BOX_SIZE, BOX_SIZE))
                if current_mode == "E":
                   main_window.blit(v_gear_big,pygame.Rect(start_x-92, start_y-92, BOX_SIZE, BOX_SIZE))
                if current_mode == "R":
                    main_window.blit(start_tile,pygame.Rect(start_x, start_y, BOX_SIZE, BOX_SIZE))
                if current_mode == "A":
                   main_window.blit(h_gear,pygame.Rect(start_x, start_y, BOX_SIZE, BOX_SIZE))
                if current_mode == "S":
                   main_window.blit(h_gear_med,pygame.Rect(start_x-48, start_y, BOX_SIZE, BOX_SIZE))                    
                if current_mode == "D":
                   main_window.blit(h_gear_big,pygame.Rect(start_x-92, start_y, BOX_SIZE, BOX_SIZE))
                if current_mode == "F":
                   main_window.blit(end_tile,pygame.Rect(start_x, start_y, BOX_SIZE, BOX_SIZE))
                if current_mode == "X":
                    color = pygame.Color(0,0,0,0)
                    pygame.draw.rect(main_window,color,(start_x,start_y,BOX_SIZE,BOX_SIZE))


                draw_grid(main_window)
                pygame.display.update()
