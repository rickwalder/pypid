import numpy as np

class pid:
    def __init__(self, kp, ki, kd, dt, dim=2):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.diffs = []
        self.zero = (0, ) * dim
        
    def updateDiff(self, sp, pv):
        diff = tuple(map(lambda x, y: x-y, sp, pv))
        self.diffs.append(diff)
        
    def calcP(self):
        fp = tuple(map(lambda x: x*self.kp, self.diffs[-1]))
        return fp
        
    def calcI(self):
        integral_prod = tuple(map(sum, zip(*self.diffs[-100:])))
        fi = tuple(map(lambda x: self.ki*x*self.dt, integral_prod))
        return fi
        
    def calcD(self):
        if not(len(self.diffs) < 2):
            fd = tuple(map(lambda x, y: self.kd*(x-y)/self.dt, self.diffs[-1], self.diffs[-2]))
            return fd
        else:
            return self.zero

    def doControlLoop(self, sp, pv):
        self.updateDiff(sp, pv)
        fp = self.calcP()
        fi = self.calcI()
        fd = self.calcD()
        
        return tuple(map(sum, zip(fp, fi, fd)))
        
    def getPosErr(self):
        return np.sqrt(self.diffs[-1][0]**2 + self.diffs[-1][1]**2)
