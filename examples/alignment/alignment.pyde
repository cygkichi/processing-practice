add_library('gifAnimation')

def cassinian(u,c1=10,c2=1):
    p = 2.0*PI*u+1
    a = c1*c1*cos(2*p)*cos(2*p)+c2
    b = c1*cos(2*p)
    r = sqrt(b+sqrt(a))
    return r*cos(p), r*sin(p)

def A(x):
    return 100*x+500

def calc_rs(xs, ys):
    N  = len(xs)
    rs = []
    for i in range(N):
        dx = xs[i] - xs[i-1]
        dy = ys[i] - ys[i-1]
        r  = sqrt(dx*dx+dy*dy)
        rs.append(r)
    return rs

def calc_ts(xs, ys):
    rs  = calc_rs(xs, ys)
    N   = len(xs)
    txs = []
    tys = []
    for i in range(N):
        dx = xs[i] - xs[i-1]
        dy = ys[i] - ys[i-1]
        tx = dx / rs[i]
        ty = dy / rs[i]
        txs.append(tx)
        tys.append(ty)
    return txs, tys

def calc_thetas(xs, ys):
    """ ref.p157 """
    thetas = []
    txs, tys = calc_ts(xs, ys)
    for tx,ty in zip(txs, tys):
        theta = acos(tx) if ty>0 else -acos(tx)
        thetas.append(theta)
    return thetas

def calc_phis(xs,ys):
    """ p158 """
    N = len(xs)
    thetas = calc_thetas(xs,ys)
    phis = []
    for i in range(N):
        if i==N-1:
            phi = thetas[0] - thetas[i]
        else:
            phi = thetas[i+1] - thetas[i]
        phi += -2*PI if phi >  PI else 0
        phi +=  2*PI if phi < -PI else 0
        phis.append(phi)
    return phis

def calc_sincostan(xs,ys):
    """ ref.p159 """    
    phis = calc_phis(xs,ys)
    sins = [sin(phi/2) for phi in phis]
    coss = [cos(phi/2) for phi in phis]
    tans = [tan(phi/2) for phi in phis]
    return sins, coss, tans

def calc_kais(xs, ys):
    """ ref.p160(7.7) """
    N = len(xs)
    rs       = calc_rs(xs,ys)
    _,_,tans = calc_sincostan(xs,ys)
    kais = [(tans[i]+tans[i-1])/rs[i] for i in range(N)]
    return(kais)

def calc_Ldot(kais,vms,rs):
    """ ref.p163(7.16) """
    N = len(kais)
    Ldot = 0.0
    for i in range(N):
        Ldot += kais[i]*vms[i]*rs[i]
    return Ldot

def calc_vs(vms,coss):
    """ ref.p161(7.13) """
    N = len(vms)
    vs = []
    for i in range(N):
        if i == N-1:
            v = (vms[i] + vms[0])/(2*coss[i])
        else:
            v = (vms[i] + vms[i+1])/(2*coss[i])
        vs.append(v)
    return vs

def calc_psis(Ldot,N,vs,sins,rs, omega):
    N = len(rs)
    L = sum(rs) # koko
    psis = [0]
    for i in range(1,N):
        psi  = Ldot/float(N) \
               -vs[i]*sins[i] \
               -vs[i-1]*sins[i-1] \
               +(L/float(N)-rs[i])*omega
        psis.append(psi)
    return psis

def calc_bigpsis(psis):
    N = len(psis)
    bigpsis = []
    for i in range(N):
        bigpsis.append(sum(psis[:i]))
    return bigpsis

def calc_c(bigpsis, coss):
    N = len(bigpsis)
    up = 0.0
    low = 0.0
    for i in range(N):
        up  += bigpsis[i]/coss[i]
        low += 1.0/coss[i]
    return -up/low   

def calc_ws(bigpsis, coss, c):
    N = len(bigpsis)
    ws = []
    for i in range(N):
        w = (bigpsis[i] + c)/coss[i] 
        ws.append(w)
    return ws

def calc_ws2(psis, coss):
    N = len(psis)
    ws = [0]
    for i in range(1,N):
        w = (ws[-1]*coss[i-1]+psis[i])/coss[i]
        ws.append(w)
    mean_w = sum(ws) / float(N)
    ws = [w - mean_w for w in ws]
    return ws

def calc_bigt(txs, tys, coss):
    N = len(txs)
    bigtxs = []
    bigtys = []
    for i in range(N):
        if i == N-1:
            bigtx = (txs[i] + txs[0])/(2*coss[i])
            bigty = (tys[i] + tys[0])/(2*coss[i])
        else:
            bigtx = (txs[i] + txs[i+1])/(2*coss[i])
            bigty = (tys[i] + tys[i+1])/(2*coss[i])
        bigtxs.append(bigtx)
        bigtys.append(bigty)
    return bigtxs, bigtys

# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
N     = 100
istep = 1
us = [i/float(N) for i in range(N)]
xs = [cassinian(u)[0] for u in us]
ys = [cassinian(u)[1] for u in us]
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def setup():
    global gifMaker
    size(1000, 1000)
    gifMaker = GifMaker(this, "alignment.gif")
    gifMaker.setRepeat(0)
    gifMaker.setDelay(10)

def draw():
    background(255, 204, 0)
    vms   = [0.1 for i in range(N)]
    omega = 10.0
    tau   = 0.005
    rs       = calc_rs(xs,ys)
    txs, tys = calc_ts(xs,ys)
    thetas   = calc_thetas(xs,ys)
    phis     = calc_phis(xs,ys)
    sins,coss,tans \
             = calc_sincostan(xs,ys)
    kais     = calc_kais(xs, ys)
    Ldot     = calc_Ldot(kais,vms,rs)
    vs       = calc_vs(vms,coss)
    psis     = calc_psis(Ldot,N,vs,sins,rs,omega)
    bigpsis  = calc_bigpsis(psis)
    c        = calc_c(bigpsis, coss)
    #ws       = calc_ws(bigpsis, coss, c)
    ws       = calc_ws2(psis, coss)
    bigtxs, bigtys = calc_bigt(txs, tys, coss)
    for i in range(N):
        x0,y0 = xs[i-1], ys[i-1]
        x1,y1 = xs[i],   ys[i]
        xm,ym = (x1+x0)/2, (y1+y0)/2
        w     = ws[i]
        fill(255)
        line(A(x1),A(y1),A(x0),A(y0))
        fill('#12ff12')
        circle(A(x1), A(y1), 10)
        fill(255)
        circle(A(xm), A(ym), 5)
        fill(0)
        textSize(12)
        
        #text("index:%d\n%.1f[deg]\ncosi:%.1f\nWi:%.10f"%(i,180*phis[i]/PI,coss[i],ws[i]),A(x1),A(y1))
        #text("kai:%.2f"%(kais[i]),A(xm),A(ym-30))
        #text("r:%1.4f"%(rs[i]),A(xm),A(ym))
    text("L: %.2f"%(sum(rs)), 0, 900)
        
    # time evo
    for i in range(N):
        x1,y1 = xs[i],   ys[i]
        x2,y2 = xs[i]+ws[i]*bigtxs[i]*tau*1000,ys[i]+ws[i]*bigtys[i]*tau*1000
        fill('#1212ff')
        #line(A(x1),A(y1),A(x2),A(y2))
        #circle(A(x2), A(y2), 5)
        xs[i] += ws[i]*bigtxs[i]*tau
        ys[i] += ws[i]*bigtys[i]*tau

    gifMaker.addFrame()
    if (frameCount > 500):
        gifMaker.finish()
        exit()   
