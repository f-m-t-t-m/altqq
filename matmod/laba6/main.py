import random
import numpy as np
from math import *
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy import interpolate


def u(x, y):
    return -pi * sin(2 * pi * x) * cos(pi * y)


def v(x, y):
    return 2 * pi * cos(2 * pi * x) * sin(pi * y)


def c(y):
    return -1 if y < 0.5 else 1


xs = []
ys = []
cs = []

random.seed(1)

for i in range(0, 1000):
    xs.append(random.random())
    ys.append(random.random())
    cs.append(c(ys[-1]))


def ode(y, t):
    x_, y_ = y
    dydt = [u(x_, y_), v(x_, y_)]
    return dydt


t = np.linspace(0, 10, 100)
y0 = list(zip(xs, ys))
res = []

for ic in y0:
    res.append(odeint(ode, ic, t))

xs_ = []
ys_ = []
for i in range(0, 1000):
    xs_.append(res[i][1][0])
    ys_.append(res[i][1][1])

xx = np.linspace(np.min(xs_), np.max(xs_))
yy = np.linspace(np.min(ys_), np.max(ys_))
xx, yy = np.meshgrid(xx, yy)
cs = np.asarray(cs)
print(cs)
xs_ = np.asarray(xs_)
ys_ = np.asarray(ys_)

vals = interpolate.griddata((xs_, ys_), cs, (xx, yy),
                            method="linear")

plt.contourf(xx, yy, vals)
plt.tight_layout()
plt.colorbar()
plt.show()
plt.savefig("6.svg")
