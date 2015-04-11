import pygame
from pygame.locals import *
pygame.init()

class InputManager:

    def __init__(self, speed):
        self.speed = speed

    def getSpeed(self):
        return self.speed

gameDisplay = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)

pacManImg = pygame.image.load('Pacman_sprite.png').convert_alpha()

ladderImg = pygame.image.load('ladder.png').convert_alpha()

def pacMan(x, y):
    gameDisplay.blit(pacManImg, (x, y))

x,y = 0,0
moveX,moveY = 0,0
screenX,screenY = gameDisplay.get_size()

gameLoop = True
while gameLoop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveX = -3
            if event.key == pygame.K_RIGHT:
                moveX = 3
            if event.key == pygame.K_UP:
                moveY = -3
            if event.key == pygame.K_DOWN:
                moveY = 3
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                moveX = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                moveY = 0

    x += moveX
    y += moveY

    gameDisplay.fill(black)
    gameDisplay.blit(ladderImg, (100,0))
    pacMan(x, y)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
