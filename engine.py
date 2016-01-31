#!/usr/bin/python

# python modules
import sys 
# library modules
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
# user modules

# game states
import ppgame, ponggl

GWindowSize = (640,480)
GCurrentState = ponggl # initial state
GLoop = True

def fnChangeGameState(state):
    global GCurrentState
    rv = True

    rv = GCurrentState.fnCleanup()
    GCurrentState = state
    rv = GCurrentState.fnInit()
    return rv # success

def main():
    global GCurrentState
    global GWindowSize
    global GLoop
    windowSize = GWindowSize
    windowFlags = OPENGL | DOUBLEBUF

    # Initialize
    pygame.init()
    screen = pygame.display.set_mode(windowSize, windowFlags)
    pygame.display.set_caption('Pong Pong')
    GCurrentState.fnInit()

    # Main game loop
    getTicksLastFrame = 0
    while GLoop:
        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0      

        if GCurrentState is None:
            sys.exit("Err: GCurrentState is empty.")

        # EVENTS
        for event in pygame.event.get():
            if event.type == QUIT:
                GLoop = False
            else:
                GCurrentState.fnEvent(event)
        
        # UPDATE
        GCurrentState.fnUpdate(deltaTime)

        # RENDER
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        GCurrentState.fnRender()
        pygame.display.flip() # buffer swap

        getTicksLastFrame = t

    pygame.quit()
    quit()
    return

if __name__ == '__main__': main()