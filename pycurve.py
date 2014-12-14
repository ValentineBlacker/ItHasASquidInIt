############################
#Metadata-Version: 1.1
#Name: pycurve
#Version: 1.0.2
#Summary: curves for python
#Home-page: http://code.google.com/p/pycurve/
#Author: Chandler Armstrong
#Author-email: omni.armstrong@gmail.com
#License: UNKNOWN
#Download-URL: http://code.google.com/p/pycurve/downloads/list
#Description: UNKNOWN
#Platform: UNKNOWN
#Classifier: Development Status :: 5 - Production/Stable
#Classifier: License :: OSI Approved :: GNU General Public License (GPL)
#Provides: pycurve
#############################



from __future__ import division
from math import factorial

PATHS = [
        [(0, 120), (100,30), (210,260),(520,575), (740,650), (870,550),(1040,260),(1050,100), (1210,50), (1280, 100)],
        [(0,450),(110,640),(270,540),(330,380),(360,260),(440,100),(700,250),(870,460),(990,590),(1280,615)],
        [(0,345),(140,320),(215,560),(430,765),(540,630),(595,390),(900,170),(1070,0),(1210,30),(1280,50)],
        [(0, 650),(155,615),(230,340),(225,530),(560,340),(770,175),(945,190),(1030,420),(1160,525),(1280,480)],
        [(0,200),(140,100),(530,40),(710,70),(790,360),(860,530),(965,650),(1080,650),(1220,650),(1280,700)],
        [(0,20),(50,10),(115,430),(150,580),(210,650),(420,730),(610,650),(900,650),(1120,650),(1280,650)],
        [(0,280),(120,155),(265,10),(330,50),(380,370),(485,650),(705,650),(1100,650),(1190,315),(1280,345)]         
         ]
for p in PATHS:
    p.reverse()

_unzip = lambda zipped: zip(*zipped) # unzip a list of tuples

def _C(n, k):
    # binomial coefficient == n! / (i!(n - i)!)
    return factorial(n) / (factorial(k) * factorial(n - k))
##############################################################

class Bspline(object):

    def __init__(self, P, t, k = None):        
        m, n = len(t) - 1, len(P) - 1
        if not k: k = m - n - 1
        else: assert m == n + k + 1
        self.k, self.t = k, t
        self.X, self.Y = _unzip(P) # points in X, Y components
        self._deboor() # evaluate

    def __call__(self, t_):
        """
        S(t) = sum(b[i][k](t) * P[i] for i in xrange(0, n))
        domain: t in [t[k - 1], t[n + 1]]

        returns point on Bspline at t_
        """
        k, t = self.k, self.t
        m = len(t) - 1
        n = m - k - 1
        assert t[k - 1] <= t_ <= t[n + 1] # t in [t[k - 1], t[n + 1]]
        X, Y, b = self.X, self.Y, self.b
        x, y, _n = 0, 0, xrange(n + 1) # initial return values, iterator over P
        for i in _n:
            b_i = b[i][k](t_)
            x += X[i] * b_i
            y += Y[i] * b_i
        return x, y

    def _deboor(self):
        # de Boor recursive algorithm
        # S(t) = sum(b[i][k](t) * P[i] for i in xrange(0, n))
        #
        # b[i][k] = {
        #     if k == 0:
        #         t[i] <= t_ < t[i+1]
        #     else:
        #         a[i][k](t)*b[i][k-1](t)+(1-a[i+1][k](t))*b[i+1][k-1](t)
        # }
        #
        # a[i][k] = {
        #     if t[i] == t[i+k]:
        #         0
        #     else:
        #         (t_-t[i])/(t[i+k]-t[i])
        # }
        #
        # NOTE: for b[i][k](t), must iterate to t[:-1];
        # the number of [i, i + 1) spans in t
        k, t = self.k, self.t
        m = len(t) - 1 # iterate to t[:-1]
        a, b, _k_, _m_ = [], [], xrange(k + 1), xrange(m)
        for i in _m_:
            a.append([]); b.append([]) # a[i]; b[i]
            for k in _k_:
                a[i].append(None) # a[i][k]
                # if k == 0: b[i][k](t) is a step function in [t[i], t[i + 1])
                if k == 0: b[i].append(lambda t_, i=i: t[i] <= t_ < t[i + 1])
                # if m < i + k: b[i][k](t) undefined
                elif m < i + k: b[i].append(lambda t_: False)
                # else: calculate b[i][k](t)
                else:
                    # if t[i] == t[i + k]: a[i][k] undefined
                    if t[i] == t[i + k]: a[i][k] = lambda t_: False
                    # else: calculate a[i][k](t)
                    else:
                        # a[i][k](t) = (t_ - t[i]) / (t[i + k] - t[i])
                        a[i][k] = lambda t_, i=i, k=k: ((t_ - t[i]) /
                                                        (t[i + k] - t[i]))
                    # b[i][k](t) = a[i][k](t) * b[i][k - 1](t) +
                    #              (1 - a[i + 1][k](t)) * b[i + 1][k - 1](t)
                    b[i].append(lambda t_, i=i, k=k:
                                a[i][k](t_) * b[i][k - 1](t_) +
                                (1 - a[i + 1][k](t_)) * b[i + 1][k - 1](t_))
        self.b = b

    def insert(self, t_):
        """
        Q[i] = (1 - a[i][k]) * P[i] + a[i][k] * P[i]
        domain: t in (t[0], t[m])

        insert new control point at t_
        """
        t = self.t
        assert t[0] < t_ < t[-1] # t_ in (t[0], t[m])
        X, Y, k = self.X, self.Y, self.k
        m = len(t) - 1
        _t_ = xrange(m + 1)
        # find the span containing t_
        for i in _t_:
            if t[i] <= t_ < t[i + 1]: break
        assert not i < k + 1 and not i > m - k + 1 # i not in clamp
        Q_x, Q_y = [], [] # new control points
        # iterate over replaced control points
        # set new control points
        for j in xrange(i - k + 1, i + 1):
            a_j = (t_ - t[j]) / (t[j + k] - t[j])
            Q_x.append((1 - a_j) * X[j - 1] + a_j * X[j])
            Q_y.append((1 - a_j) * Y[j - 1] + a_j * Y[j])
        Q_x, Q_y = tuple(Q_x), tuple(Q_y)
        self.t = t[:i + 1] + [t_] + t[i + 1:]
        self.X = X[:i - k + 1] + Q_x + X[i:]
        self.Y = Y[:i - k + 1] + Q_y + Y[i:]
        self._deboor() # re-evaluate

################################################################################
def make_b_spline(scene, P):
    STEP_N = int((scene.field_length/2)- scene.wave_number*20)
    
    
    
    n = len(P) - 1 # n = len(P) - 1; (P[0], ... P[n])
    k = 3          # degree of curve
    m = n + k + 1  # property of b-splines: m = n + k + 1
    _t = 1 / (m - k * 2) # t between clamped ends will be evenly spaced
    # clamp ends and get the t between them
    t = k * [0] + [t_ * _t for t_ in xrange(m - (k * 2) + 1)] + [1] * k

    S = Bspline(P, t, k)
    # insert a knot (just to demonstrate the algorithm is working)
    S.insert(0.9)

    patharray = []
    
    step_size = 1 / STEP_N
    for i in xrange(STEP_N):
        t_ = i * step_size
        try: x, y = S(t_)
        # if curve not defined here (t_ is out of domain): skip
        except AssertionError: continue
        x, y = int(x), int(y)        
        patharray.append((x,y))
        
    return patharray
   
   

 

