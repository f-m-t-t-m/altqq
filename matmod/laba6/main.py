import math
import random
import numpy as np
from math import *
import matplotlib.pyplot as plt
from scipy.integrate import odeint, RK45
from scipy import interpolate

x, y = np.meshgrid(
    np.linspace(0, 1, 20),
    np.linspace(0, 1, 20)
)

u = -np.pi * np.sin(2 * np.pi * x) * np.cos(np.pi * y)

v = 2 * np.pi * np.cos(2 * np.pi * x) * np.sin(np.pi * y)



plt.figure()
# plt.quiver(x, y, u, v, color='b')
plt.streamplot(x,y,u,v, density=1.4, linewidth=None, color='#A23BEC')
plt.tight_layout()
plt.grid()
plt.savefig("11.png")


# def c(y):
#     return atan((y-0.5)/0.1)
#
# # def c(y):
# #     return -1 if y < .5 else 1
#
# xs = []
# ys = []
# cs = []
#
# random.seed(1)
#
# for i in range(0, 10000):
#     xs.append(random.random())
#     ys.append(random.random())
#     cs.append(c(ys[-1]))
#
# def ode(y, t):
#     x_, y_ = y
#     dydt = [u(x_, y_), v(x_, y_)]
#     return dydt
#
#
# t = np.linspace(0, 1, 100)
# y0 = list(zip(xs, ys))
# res = []
#
# for ic in y0:
#     res.append(RK45(ode, ic, t))
#
# xs_ = []
# ys_ = []
# for i in range(0, 10000):
#     xs_.append(res[i][99][0])
#     ys_.append(res[i][99][1])
#
# xx = np.linspace(np.min(xs_), np.max(xs_), 1000)
# yy = np.linspace(np.min(ys_), np.max(ys_), 1000)
# xx, yy = np.meshgrid(xx, yy)
#
# cs = np.asarray(cs)
# xs_ = np.asarray(xs_)
# ys_ = np.asarray(ys_)
#
# vals = interpolate.griddata((xs_, ys_), cs, (xx, yy),
#                            method="linear")
#
# plt.figure()
# plt.pcolormesh(xx, yy, vals)
# plt.tight_layout()
# plt.colorbar()
# plt.savefig("10.png")
