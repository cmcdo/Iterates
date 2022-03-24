import pygame as pg
import pygame.gfxdraw
import math
W, H = 1200, 800
display = pg.display.set_mode((W, H), pg.RESIZABLE)
pg.display.set_caption("Iterates of D")
r = True


def aafilledcircle(surf, x, y, r, col):
    pg.gfxdraw.aacircle(surf, x, y, r, col)
    pg.gfxdraw.filled_circle(surf, x, y, r, col)

"""
Unit Circle Stuff.
"""
pad = 20
rad = 1
def drawD(surf):
    global rad
    rad = H//2 - pad
    pg.gfxdraw.aacircle(surf, W//2, H//2, rad,  (0, 0, 0)) 


#IterateInformation
theta = 1.57
a = [1/2, 1/2]

def drawPara(surf):
    acords = plane2screen(a[0], a[1])
    ucords = plane2screen(math.cos(theta), math.sin(theta))
    aafilledcircle(surf, acords[0], acords[1], 2, (0, 0, 0))
    aafilledcircle(surf, ucords[0], ucords[1], 2, (0,0,0))


#ScreenScaling

def screen2plane(x, y):
    return (int((x - W//2)/rad), int(-(y - H//2)/rad))

def plane2screen(x,y):
    return (int(rad*x+W//2), int(-rad*y+H//2))


while r:
    W, H = display.get_size()
    mx, my = pg.mouse.get_pos()
   
    for e in pg.event.get():
        if e.type == pg.QUIT:
            r = False
   
    display.fill((255, 255, 255))
    drawD(display)
    drawPara(display)
    pg.display.flip()

quit()
