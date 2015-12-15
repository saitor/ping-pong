import pygame, math, sys
from pygame.locals import *

WIDTH = 1024
HEIGHT = 768
TURN_SPEED = 5
ACCELERATION = 2
MAX_FORWARD_SPEED = 10
MAX_REVERSE_SPEED = 5
BGCOLOR = (20,50,80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

while 1:
    ### EVENT ###
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: 
            if event.key == K_ESCAPE: 
                sys.exit(0)
        elif event.type == pygame.QUIT:
            sys.exit(0)

    ### UPDATE ###

    ### RENDER ###
    screen.fill(BGCOLOR)
    pygame.display.flip()
