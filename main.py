import pygame as pg
import pygame.gfxdraw
import math
W, H = 1200, 800
display = pg.display.set_mode((W, H), pg.RESIZABLE)
pg.display.set_caption("Iterates of D")
r = True

def dist(x, y):
    return ((x[0]-y[0])**2 + (x[1] - y[1])**(2))**(1/2) 

def aafilledcircle(surf, x, y, r, col):
    pg.gfxdraw.aacircle(surf, x, y, r, col)
    pg.gfxdraw.filled_circle(surf, x, y, r, col)

"""
Unit Circle Stuff.
"""
pad = 200
rad = 2
def drawD(surf):
    global rad
    rad = H//2 - pad
    pg.gfxdraw.aacircle(surf, W//2, H//2, rad,  (0, 0, 0)) 


#IterateInformation
theta = 0 
a = [1/2, 0]
thetaHeld = False
aHeld = False
z0 = [0, 0]
z0Held = False
def drawPara(surf):
    acords = plane2screen(a[0], a[1])
    ucords = plane2screen(math.cos(theta), math.sin(theta))
    aafilledcircle(surf, acords[0], acords[1], 2, (0, 0, 0))
    aafilledcircle(surf, ucords[0], ucords[1], 2, (0,0,0))


#ScreenScaling

def screen2plane(x, y):
    return ((x - W//2)/rad, -(y - H//2)/rad)

def plane2screen(x,y):
    return (int(rad*x+W//2), int(-rad*y+H//2))

#ParaChanging
def changingTheta():
    global theta, thetaHeld 
    mx, my = pg.mouse.get_pos()
    mb1 = pg.mouse.get_pressed()[0]    
    ucord = plane2screen(math.cos(theta), math.sin(theta))
    distance = dist([mx, my], ucord)
    if thetaHeld:
        theta = -math.atan2(my - H//2, mx - W//2)
    
    if thetaHeld and mb1 != 1:
        thetaHeld = False

        
def changingA():
    global a, aHeld 
    mx, my = pg.mouse.get_pos()
    mb1 = pg.mouse.get_pressed()[0]    
    acord = plane2screen(a[0], a[1])
    distance = dist([mx, my], acord)
    if aHeld:
        if dist(screen2plane(mx, my), [0, 0]) <=1:
            a = screen2plane(mx, my)

    if aHeld and mb1 != 1:
        aHeld = False

def changingZ0():
    global z0, z0Held 
    mx, my = pg.mouse.get_pos()
    mb1 = pg.mouse.get_pressed()[0]    
    z0cord = plane2screen(z0[0], z0[1])
    distance = dist([mx, my], z0cord)
    if z0Held:
        if dist(screen2plane(mx, my), [0,0]) <= 1:
            z0 = screen2plane(mx, my)

    if z0Held and mb1 != 1:
        z0Held = False


#Mobius and Complex math
    
def complexAbs(z):
    return (z[0]**2 + z[1]**2)**(1/2)

def complexAdd(z, w):
    return [z[0] + w[0], z[1] + w[1]]

def complexMinus(z, w):
    return [z[0] - w[0], z[1] - w[1]]

def complexInvert(z):
    absc = complexAbs(z)**2
    return [z[0]/absc, - z[1]/absc]

def complexMultiply(z, w):
    return [z[0]*w[0] - z[1]*w[1], z[0]*w[1] + z[1] * w[0]] 

def complexDivide(z, w):
    return complexMultiply(z, complexInvert(w))


def complexpow(z, n):
    r = complexAbs(z)**(n)
    t  = math.atan2(z[1], z[0])
    return [r*math.cos(t*n), r*math.sin(t*n)]

def mob(z):
    u = [math.cos(theta), math.sin(theta)]
    nume = complexMinus(complexMultiply(u,z), complexMultiply(u, a))
    denom = complexMinus([1, 0], complexMultiply(z, [a[0], -a[1]]))
    return complexDivide(nume, denom)

def mobList(z0, n):
    iterateList = [z0]
    z = z0
    for i in range(n):
        val = mob(z)
        iterateList.append(val)
        z = val 
    return iterateList

def plotPoints(surf):
    iterates = mobList(z0, 1000)
    for iterate in iterates:
        icord = plane2screen(iterate[0], iterate[1])
        aafilledcircle(surf, icord[0], icord[1], 2, (0, 0, 0))


def plotPoint(surf, x):
    x = plane2screen(x[0], x[1])
    aafilledcircle(surf, x[0], x[1], 2, (0, 0, 0))

def computingFixedPoints():
    u = [math.cos(theta), math.sin(theta)]
    um12 = complexpow(complexMinus(u,[1,0]) , 2)
    fua2 = complexMultiply(u, [4*complexAbs(a)**2, 0])
    rootterm = complexpow(complexAdd(um12, fua2), 1/2)
    
    r1 = complexDivide(complexAdd(complexMinus([1,0],u),rootterm),complexMultiply([2, 0],[a[0], -a[1]]))
    r2 = complexDivide(complexMinus(complexMinus([1,0],u),rootterm),complexMultiply([2, 0],[a[0], -a[1]])) 
    
    return [r1, r2]

while r:
    W, H = display.get_size()
    mx, my = pg.mouse.get_pos()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            r = False
        
        if e.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0] == 1:
                if dist([mx, my], plane2screen(math.cos(theta), math.sin(theta))) <= 20:
                    thetaHeld = True
                if dist([mx, my], plane2screen(a[0], a[1])) <= 20:
                    aHeld = True
                if dist([mx, my], plane2screen(z0[0], z0[1])) <= 20:
                    z0Held = True


    display.fill((255, 255, 255))
    drawD(display)
    drawPara(display)
    changingTheta()
    changingA()
    changingZ0()
    plotPoints(display)
    plotPoint(display, computingFixedPoints()[1])
    pygame.gfxdraw.aacircle(display, W//2, H//2, int(rad * abs(math.sin(theta/2))), (0, 255, 0))
    pg.display.flip()

quit()
