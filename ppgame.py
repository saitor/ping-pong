#!/usr/bin/python

# python modules
import sys 
# library modules
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
# user modules
import engine

GVerticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

GEdges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

GAngles = 0

##################################
# Local functions
##################################


##################################
# Essential game state functions
##################################
def fnInit():
    ws = engine.GWindowSize
    gluPerspective(75, (ws[0]/ws[1]), 0.1, 50.0)

def fnEvent(event):
    if event.type == pygame.QUIT:
        engine.GLoop = False

    return

def fnUpdate(timedelta):
    pygame.time.wait(10)
    return

def fnRender():
    global GAngles

    glPushMatrix()
    glTranslatef(0.0, 0.0, -7.0)
    glRotatef(GAngles, 0, 1, 0)

    # Draw cube
    glBegin(GL_LINES)
    for edge in GEdges:
        for vertex in edge:
            glVertex3fv(GVerticies[vertex])
    glEnd()

    glPopMatrix()
    GAngles = GAngles + 1.2
    return

def fnCleanup():
    return