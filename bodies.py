import math

class pointMass:

    def __init__(self, m=5.0, r=(0, 0),
                 a=(0, 0), v=(0, 0), f=[]):
        self.d = 2 # experimental
        self.m = m
        self.f = []
        self.a = a
        self.v = v
        self.r = r
        self.applyForce((0, ) * self.d)
        
    def applyForce(self, fnew):
        self.f.append(fnew)

    def stepTime(self, dt):
        # calculate acceleration
        # a = f/m
        f_net  = tuple(map(math.fsum, zip(*self.f)))
        self.a = tuple(map(lambda x: x/self.m, f_net))

        # calculate new position
        # dr = v_0 * t + 1/2at^2
        v0t = tuple(map(lambda x: x*dt, self.v))
        at2 = tuple(map(lambda x: 0.5*x*dt*dt, self.a))
        dr = tuple(map(math.fsum, zip(v0t, at2)))
        self.r = tuple(map(math.fsum, zip(self.r, dr)))

        # calculate new velocity
        # v = v_0 + at
        dv = tuple(map(lambda x: x*dt, self.a))
        self.v = tuple(map(math.fsum, zip(self.v, dv)))
        
        # reset f to zero
        self.f = [(0, ) * self.d]
        return dt
