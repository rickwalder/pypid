from bodies import pointMass
from control import pid
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import math

import random

#random.seed("tacos")

from plotUtils import BlitManager



# set up masses, pm is setpoint, ctrl is process value
pm = pointMass(m=1, v=(0, 0), r=(1, 0))
t = 0
dt = 0.01
xhold1 = []
yhold1 = []
xhold2 = []
yhold2 = []

controller = pid(kp = 6.2, ki = 5.1, kd = 12.4, dt=dt, dim=2)
ctrl = pointMass(m=1)

# set up graphical environment

fig, ax = plt.subplots()
fi2     = plt.figure(2)
a2      = fi2.add_subplot()

# animated=True tells matplotlib to only draw the artist when we
# explicitly request it
#v     = ax.quiver(ctrl.r, [1, 1])
(p1,) = ax.plot([0], [0], marker='o', animated=True)
(t1,) = ax.plot([0], [0], animated=True)
(p2,) = ax.plot([0], [0], marker='o', animated=True)
(t2,) = ax.plot([0], [0], animated=True)
(err,)= a2.plot([0], [0], animated=True)

bm = BlitManager(fig.canvas, [p1, t1, p2, t2])
bm2 = BlitManager(fi2.canvas, [err])
ax.axis('equal')
# ax.autoscale()
ax.set(ylim=(.75, 1.25), xlim=(-2, 2))
a2.set(xlim=(0, 50), ylim=(0, 1))
#a2.set_yscale("log")
plt.show(block=False)
plt.pause(0.1)

diffs = []
forces = []
skip_d = True
posn_err = []
times = []

for i in range(10000):
    # move the reference point around directly by assiging its r vector
    # apply some random force to the reference point
    pm.r = (0, 1)#(np.cos(t), np.sin(2*t))
    #forces.append((random.triangular(-0.1, 0.1) - 0.001*pm.r[0], random.triangular(-0.1, 0.1) - 0.009*pm.r[1]))
    #print(forces)
    #pm.f = forces[-10:]
    #pm.applyForce((-np.cos(t), -np.sin(t)))
    #print(pm.a)
    #ctrl.f = forces[-20:]
    
    ctrl.applyForce(controller.doControlLoop(pm.r, ctrl.r))
    posn_err.append(controller.getPosErr())
    
    # step time
    pm.stepTime(dt)
    t = math.fsum((t, ctrl.stepTime(dt)))
    times.append(t)
    if pm.r == ctrl.r:
        print("winning")
        
    # append position to tracks
    xhold1.append(pm.r[0])
    yhold1.append(pm.r[1])
    xhold2.append(ctrl.r[0])
    yhold2.append(ctrl.r[1])
    
    p1.set_xdata(pm.r[0])
    p1.set_ydata(pm.r[1])
    t1.set_xdata(xhold1[-100:])
    t1.set_ydata(yhold1[-100:])
    p2.set_xdata(ctrl.r[0])
    p2.set_ydata(ctrl.r[1])
    t2.set_xdata(xhold2[-100:])
    t2.set_ydata(yhold2[-100:])
    err.set_xdata(times)
    err.set_ydata(posn_err)
    # update the screen
    bm.update()
    bm2.update()
