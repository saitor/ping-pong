#!/usr/bin/python

# python modules
import sys, math
# library modules
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
# user modules
import engine

class csPoint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class csGameObject(object):
    def __init__(self, pos, vel):
        self.pos = pos # position
        self.vel = vel # velocity

GBarDisplay     = csPoint(10.0, 50.0)

GBackground_bl  = csPoint(5, 5)
GBackground_tr  = csPoint(635, 475)

GPlayerBar  = csGameObject(csPoint( 10.0, 215.0),csPoint(  0.0,   0.0))
GAIBar      = csGameObject(csPoint(620.0, 215.0),csPoint(  0.0,   0.0))
GBall       = csGameObject(csPoint(307.5, 232.5),csPoint(250.0, 250.0))
GBallRadius = 7.0

GPlayerScore    = 0
GAIScore        = 0

GBarSpeed       = 250.0

##################################
# Local functions
##################################

def lfnDrawCircle(radius):
    DEG2RAD = 3.14159/180;
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0.0, 0.0)
    for i in range(0, 360):
        degInRad = i*DEG2RAD
        glVertex2f(math.cos(degInRad)*radius,math.sin(degInRad)*radius)
    glEnd()

def lfnDrawText(position, textString):
    font = pygame.font.SysFont("calibri",40)
    #font = pygame.font.Font(None, 40)
    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos2f(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def lfnAIMovement():
    global GAIBar, GBall

    # react when it is near
    if GBall.pos.x >= 305.0 and GBall.vel.x > 0:
        if not GAIBar.pos.y == GBall.pos.y + 7.5:
            if GAIBar.pos.y < GBall.pos.y + 7.5:
                GAIBar.vel.y = GBarSpeed
            if  GAIBar.pos.y > GBall.pos.y - 42.5:
                GAIBar.vel.y = -GBarSpeed
        else:
            GAIBar.pos.y = GBall.pos.y + 7.5
    else:
        GAIBar.vel.y = 0.0

##################################
# Essential game state functions
##################################
def fnInit():
    ws = engine.GWindowSize
    gluOrtho2D(0,ws[0],0,ws[1])

def fnEvent(event):
    global GBarSpeed

    if event.type == KEYDOWN:
        if event.key == K_UP:
            GPlayerBar.vel.y = GBarSpeed
        elif event.key == K_DOWN:
            GPlayerBar.vel.y = -GBarSpeed
    elif event.type == KEYUP:
        if event.key == K_UP:
            GPlayerBar.vel.y = 0.0
        elif event.key == K_DOWN:
            GPlayerBar.vel.y = 0.0
    return

def fnUpdate(dt):
    global GPlayerBar, GAIBar, GBall
    global GPlayerScore, GAIScore
    global GBallRadius

    lfnAIMovement()

    # player
    GPlayerBar.pos.x = GPlayerBar.pos.x + GPlayerBar.vel.x*dt
    GPlayerBar.pos.y = GPlayerBar.pos.y + GPlayerBar.vel.y*dt

    # AI
    GAIBar.pos.x = GAIBar.pos.x + GAIBar.vel.x*dt
    GAIBar.pos.y = GAIBar.pos.y + GAIBar.vel.y*dt

    # ball
    GBall.pos.x = GBall.pos.x + GBall.vel.x*dt
    GBall.pos.y = GBall.pos.y + GBall.vel.y*dt

    # bar hit the frame
    if GPlayerBar.pos.y >= 420.0: GPlayerBar.pos.y = 420.0
    elif GPlayerBar.pos.y <= 10.0: GPlayerBar.pos.y = 10.0

    if GAIBar.pos.y >= 420.0: GAIBar.pos.y = 420.0
    elif GAIBar.pos.y <= 10.0: GAIBar.pos.y = 10.0

    # ball hit bar
    if GBall.pos.x <= GPlayerBar.pos.x + 10.0:
        if GBall.pos.y >= GPlayerBar.pos.y and GBall.pos.y <= GPlayerBar.pos.y + GBarDisplay.y:
            GBall.pos.x = 25.0
            GBall.vel.x = -GBall.vel.x
    if GBall.pos.x >= GAIBar.pos.x:
        if GBall.pos.y >= GAIBar.pos.y and GBall.pos.y <= GAIBar.pos.y + GBarDisplay.y:
            GBall.pos.x = 615.0
            GBall.vel.x = -GBall.vel.x

    # ball hit left and right, score
    if GBall.pos.x < 5.0:
        GAIScore += 1
        GBall.pos.x = 320.0
        GBall.pos.y = 232.5
        GPlayerBar.pos.y = GAIBar.pos.y = 215.0
    elif GBall.pos.x > 635.0:
        GPlayerScore += 1
        GBall.pos.x = 320.0
        GBall.pos.y = 232.5
        GPlayerBar.pos.y = GAIBar.pos.y = 215.0

    # ball hit top and bottom
    if GBall.pos.y <= 10.0:
        GBall.vel.y = -GBall.vel.y
        GBall.pos.y = 10.0
    elif GBall.pos.y >= 457.5:
        GBall.vel.y = -GBall.vel.y
        GBall.pos.y = 457.5

    return

def fnRender():
    global GPlayerBar, GAIBar, GBall
    global GBackground_bl, GBackground_tr
    global GBallRadius

    # draw background
    glPushMatrix()
    glColor(255, 255, 255)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glRectf(GBackground_bl.x, GBackground_bl.y, GBackground_tr.x, GBackground_tr.y)
    glBegin(GL_LINES);
    glVertex2f(330, GBackground_bl.y);
    glVertex2f(330, GBackground_tr.y);
    glEnd();
    glPopMatrix()

    # draw score
    lfnDrawText((250.0, 210.0), str(GPlayerScore))
    lfnDrawText((380.0, 210.0), str(GAIScore))

    # draw player
    glPushMatrix()
    glColor(0, 0, 255)
    glTranslatef(GPlayerBar.pos.x, GPlayerBar.pos.y, 0.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glRectf(0,0,GBarDisplay.x, GBarDisplay.y)
    glPopMatrix()

    # draw AI
    glPushMatrix()
    glColor(255, 0, 0)
    glTranslatef(GAIBar.pos.x, GAIBar.pos.y, 0.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glRectf(0,0,GBarDisplay.x, GBarDisplay.y)
    glPopMatrix()

    # draw ball
    glPushMatrix()
    glColor(0, 255, 0)
    glTranslatef(GBall.pos.x, GBall.pos.y, 0.0)
    lfnDrawCircle(GBallRadius)
    glPopMatrix()

    return

def fnCleanup():
    pass