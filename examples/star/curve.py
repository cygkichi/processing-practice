def init_shape(u):
    p = 2*PI*u + 1
    r = 0.6 + 0.3*sin(p*5)
    return r*cos(p), r*sin(p)

class Curve(object):
    def __init__(self,N=10):
        self.N   = N
        self.us  = [i/float(N) for i in range(N)]
        self.points     = [init_shape(u) for u in self.us]     
        self.calc()
        self.tau = 0.004
    
    def calc(self):
        self.midpoints  = _calc_midpoints(self.points)
        self.rs         = _calc_rs(self.points)
        self.tm_vectors = _calc_tm_vectors(self.points)
        self.nm_vectors = _calc_nm_vectors(self.tm_vectors)
        self.thetas     = _calc_thetas(self.tm_vectors)
        self.phis       = _calc_phis(self.thetas)
        self.sins       = [sin(p/2.0) for p in self.phis]
        self.coss       = [cos(p/2.0) for p in self.phis]
        self.tans       = [tan(p/2.0) for p in self.phis]
        self.kais       = _calc_kais(self.rs, self.tans)
        self.t_vectors  = _calc_t_vectors(self.tm_vectors, self.coss)
        self.n_vectors  = [[ty, -tx] for tx,ty in self.t_vectors]
        self.A          = _calc_A(self.points)
        self.G          = _calc_G(self.points, self.A)
        # calc Ws
        self.psis       = _calc_psis(self.sins, self.rs)
        self.ws         = _calc_ws(self.psis, self.coss)
        
        
    def step(self):
        for i in range(self.N):
            k=0.01
            x, y = self.points[i]
            x += self.t_vectors[i][0]*self.ws[i]*self.tau
            y += self.t_vectors[i][1]*self.ws[i]*self.tau
            if self.kais[i] < 0:
                x += -k*self.kais[i]*self.n_vectors[i][0]*self.tau  
                y += -k*self.kais[i]*self.n_vectors[i][1]*self.tau
                
            self.points[i] = [x, y] 
        self.calc()


def _calc_rs(points):
    N = len(points)
    rs = []
    for i in range(N):
        dx = points[i][0] - points[i-1][0]
        dy = points[i][1] - points[i-1][1]
        r  = sqrt(dx*dx+dy*dy)
        rs.append(r)
    return rs

def _calc_midpoints(points):
    N = len(points)
    midpoints = []
    for i in range(N):
        x0,y0 = points[i-1][0], points[i-1][1]
        x1,y1 = points[i][0]  , points[i][1]
        xm    = (x1+x0) / 2.0
        ym    = (y1+y0) / 2.0
        midpoints.append([xm, ym])
    return midpoints

def _calc_tm_vectors(points):
    N   = len(points)
    tm_vectors = []
    for i in range(N):
        dx = points[i][0] - points[i-1][0]
        dy = points[i][1] - points[i-1][1]
        r  = sqrt(dx*dx+dy*dy)
        tx = dx / r
        ty = dy / r
        tm_vectors.append([tx,ty])
    return tm_vectors

def _calc_nm_vectors(tm_vectors):
    return [[ty, -tx] for tx,ty in tm_vectors]

def _calc_thetas(tm_vectors):
    thetas = []
    for tx,ty in tm_vectors:
        theta = acos(tx) if ty>0 else -acos(tx)
        thetas.append(theta)
    return thetas

def _calc_phis(thetas):
    N = len(thetas)
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

def _calc_kais(rs, tans):
    N = len(tans)
    return [(tans[i]+tans[i-1])/rs[i] for i in range(N)]

def _calc_t_vectors(tm_vectors, coss):
    N = len(tm_vectors)
    t_vectors = []
    for i in range(N):
        if i == N-1:
            tx = (tm_vectors[i][0] + tm_vectors[0][0])/(2*coss[i])
            ty = (tm_vectors[i][1] + tm_vectors[0][1])/(2*coss[i])
        else:
            tx = (tm_vectors[i][0] + tm_vectors[i+1][0])/(2*coss[i])
            ty = (tm_vectors[i][1] + tm_vectors[i+1][1])/(2*coss[i])
        t_vectors.append([tx,ty])
    return t_vectors

def _calc_psis(sins, rs, omega=10.0):
    N = len(sins)
    L = sum(rs)
    psis = [0]
    for i in range(1,N):
        psi = (L/float(N) - rs[i])*omega
        psis.append(psi)
    return psis                

def _calc_ws(psis, coss):
    N = len(psis)
    ws = [0]
    for i in range(1,N):
        w = (ws[-1]*coss[i-1]+psis[i])/coss[i]
        ws.append(w)
    mean_w = sum(ws) / float(N)
    ws = [w - mean_w + 0.5 for w in ws]
    return ws

def _calc_A(points):
    N = len(points)
    A = 0.0
    for i in range(N):
        x0,y0 = points[i-1]
        x1,y1 = points[i]
        A += (x0*y1 - x1*y0)*0.5
    return A

def _calc_G(points, A):
    N  = len(points)
    Gx = 0.0
    Gy = 0.0
    for i in range(N):
        x0,y0 = points[i-1]
        x1,y1 = points[i]
        det = x0*y1 - x1*y0
        Gx += det*(x1 + x0)/(6*A)
        Gy += det*(y1 + y0)/(6*A)
    return [Gx,Gy]
        
        
        
