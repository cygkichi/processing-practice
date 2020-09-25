BLACK  = unhex("FF000000")
WHITE  = unhex("FFFFFFFF")

BG  = unhex("FFFBC114")

GREEN  = unhex("FF52950F")
RED    = unhex("FFDB1D08")
PINK   = unhex("FFE32190")
INDIGO = unhex("FF004876")
AMBER  = unhex("FFFFC107")
TOMATO = unhex("FFEA5549")

def T(point):
    x, y = point
    unit = min(width,height)/2.0
    return unit*x+width/2,\
          -unit*y+height/2

def draw_points(points, pc=TOMATO, lc=BLACK,ps=10):
    for p in points:
        x, y = T(p)
        fill(pc)
        stroke(lc)
        circle(x,y,ps)

def draw_lines(points, lc=BLACK):
    N = len(points)
    for i in range(N):
        x0, y0 = T(points[i-1])
        x1, y1 = T(points[i])
        stroke(lc)
        line(x0,y0,x1,y1)

def draw_vector(point, vector,
        theta = PI/6.0,
        head_size=0.02,
        length_rate=0.1,
        lc=BLACK):
    stroke(lc)
    x, y = point
    vx = vector[0] * length_rate
    vy = vector[1] * length_rate
    x0, y0 = T([x+vx, y+vy])
    x1, y1 = T(point)
    line(x0,y0,x1,y1)
    for t in [theta ,-theta]:
        ax = -cos(t)*vector[0] + sin(t)*vector[1]
        ay = -sin(t)*vector[0] - cos(t)*vector[1]
        a_length = sqrt(ax*ax+ay*ay)
        ax = ax/a_length*head_size
        ay = ay/a_length*head_size
        x0, y0 = T([x+vx   , y+vy])
        x1, y1 = T([x+vx+ax, y+vy+ay])
        line(x0,y0,x1,y1)

def draw_vectors(points, vectors,
        lc=BLACK):
    stroke(lc)
    for p,v  in zip(points, vectors):
        draw_vector(p,v)


def draw_debugtext_no(curve, no,
        ts   = 20,
        tc   = BLACK):
    textSize(ts)
    fill(tc)
    point = curve.points[no]
    x,y = T(point)
    text("IDX:%d\nPHI:%.1f[deg]"%(no,
        curve.phis[no]/PI*180),x,y)

    midpoint = curve.midpoints[no]
    xm,ym = T(midpoint)   
    text("IDX:%d\nKAI:%.1f\nl:%.2f"%(no,
        curve.kais[no],
        curve.rs[no]),xm,ym)
    
def draw_debugtext_value(curve,
        pos=[-0.7,-0.7],
        ts   = 20,
        tc   = BLACK):
    textSize(ts)
    fill(tc)
    x,y = T(pos)
    text("frameCount:%d\nL:%.2f\nA:%.2f"%(frameCount,sum(curve.rs),curve.A),x,y)
