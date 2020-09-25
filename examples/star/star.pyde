add_library('gifAnimation')
from drawtools import *
from curve import Curve

makeimg = True

def setup():
    global gifMaker,c
    size(1000, 1000)
    background(BG)
    c = Curve(N=120)
    if makeimg:
        gifMaker = GifMaker(this,"star.gif")
        gifMaker.setRepeat(0)
        gifMaker.setDelay(10)
        
def draw():
    background(BG)
    #fill(unhex("11FBC114"))
    #rect(0, 0, width, height,)
    draw_lines(c.points)
    draw_points(c.points, pc=RED, ps=12)
    draw_points(c.midpoints, pc=RED, ps=6)
    c.step()
    
    if makeimg:
        if (frameCount%80==0):
            gifMaker.addFrame()
        if (frameCount > 6000):
            gifMaker.finish()
            exit()   
