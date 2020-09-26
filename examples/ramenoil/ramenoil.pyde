add_library('gifAnimation')
from drawtools import *
from curve import Curve

makeimg = True

def setup():
    global gifMaker,c, moveFlag
    size(1000, 1000)
    background(BG)
    c = Curve(N=0)
    moveFlag = False
    if makeimg:
        gifMaker = GifMaker(this,"ramenoil.gif")
        gifMaker.setRepeat(0)
        gifMaker.setDelay(10)
         
def draw():
    background(BG)
    draw_lines(c.points)
    draw_points(c.points, pc=RED, ps=12)
    draw_debugtext_value(c)
    if moveFlag:
        for i in range(c.N*10):
            c.step(t_direction=True,n_direction=False)
        c.step(t_direction=True,n_direction=True)

    if makeimg:
        if (frameCount%10==0):
            gifMaker.addFrame()
        if (frameCount > 600000):
            gifMaker.finish()
            exit()

def mousePressed():
    if (mouseButton == LEFT):
        c.add_point(TR([mouseX, mouseY]))
        print(TR([mouseX, mouseY]))
    elif(mouseButton == RIGHT):
        c.delete_point()
        

def keyPressed():
    global moveFlag
    SPACEKEY = 32
    if keyCode == SPACEKEY:
        moveFlag = False if moveFlag else True
