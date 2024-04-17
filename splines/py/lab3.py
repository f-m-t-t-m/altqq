import math

import matplotlib.pyplot as plt
import numpy as np

def function(t):
    return 1000*math.cos(t)**3, 1000*math.sin(t)**3


def calc_mu(d: list):
    return [0] + [d[i-1] / (d[i-1]+d[i]) for i in range(1, len(d))]


def build_system(d: list, x: list):
    a = np.zeros((len(d), len(d)))
    mu = calc_mu(d)
    lambda_ = [1 - m for m in mu]

    P = [(3 + 3 * p[i] + p[i] ** 2) / ((2 + q[i]) * (2 + p[i]) - 1) for i in range(len(d))]
    Q = [(3 + 3 * q[i] + q[i] ** 2) / ((2 + q[i]) * (2 + p[i]) - 1) for i in range(len(d))]

    a[0][len(d)-1] = lambda_[1] * P[0]
    a[0][0] = lambda_[1] * P[0] * (2 + q[0]) + mu[1] * Q[1] * (2 + p[1])
    a[0][1] = mu[1] * Q[1]
    for i in range(2, len(d)):
        a[i-1][i-2] = lambda_[i]*P[i-1]
        a[i-1][i-1] = lambda_[i]*P[i-1]*(2+q[i-1]) + mu[i]*Q[i]*(2+p[i])
        a[i-1][i] = mu[i]*Q[i]

    a[len(d)-1][len(d)-2] = lambda_[len(d)-1] * P[len(d)-2]
    a[len(d)-1][len(d)-1] = lambda_[len(d)-1] * P[len(d)-2] * (2 + q[len(d)-2]) + mu[len(d)-1] * Q[len(d)-1] * (2 + p[len(d)-1])
    a[len(d)-1][0] = mu[1] * Q[len(d)-1]

    f = np.zeros(len(d))
    for i in range(1, len(d)):
        f[i-1] = lambda_[i]*P[i-1]*(3+q[i-1]) * (x[i] - x[i-1])/d[i-1] + mu[i]*Q[i]*(3+p[i]) * (x[i+1] - x[i])/d[i]
    i = len(d)-1
    f[i] = lambda_[i] * P[i] * (3 + q[i]) * (x[i] - x[i - 1]) / d[i - 1] + mu[i] * Q[i] * (3 + p[i]) * (x[1] - x[i]) / d[i]

    return a, f


def find_coef(x, m, d):
    C = [ (-(3+q[i])*(x[i+1] - x[i]) + d[i]*m[i] + (2+q[i])*d[i]*m[i+1])/((2+q[i])*(2+p[i]) - 1) for i in range(len(x)-1) ]
    D = [ ((3+p[i])*(x[i+1] - x[i]) - d[i]*m[i+1] - (2+p[i])*d[i]*m[i])/((2+q[i])*(2+p[i]) - 1) for i in range(len(x)-1) ]
    B = [x[i] - D[i] for i in range(len(D))]
    A = [x[i+1] - C[i] for i in range(len(C))]

    return A, B, C, D


def solve_system(a, f):
    m = np.linalg.solve(a, f)
    return [m[-1], *m]


def spline(s_, A, B, C, D):
    for i in range(len(s)-1):
        if s[i] <= s_ <= s[i + 1]:
            t = (s_-s[i])/d[i]
            return A[i]*t + B[i]*(1-t) + C[i]*t**3/(1+p[i]*(1-t)) + D[i]*(1-t)**3/(1+q[i]*t)


if __name__ == '__main__':
    vf = np.vectorize(function)
    ts = np.linspace(0, 2*np.pi, 100)
    x, y = vf(ts)
    d = [np.sqrt((x[i]-x[i+1])**2 + (y[i]-y[i+1])**2) for i in range(len(ts)-1)]
    s = [0]
    p = [5 for i in range(len(d))]
    p[0] = 100
    p[-1] = 100
    p[int(len(d)/2)+1] = 100
    p[int(len(d)/2)-1] = 100
    p[int(len(d)/4)+1] = 100
    p[int(len(d)/4)-1] = 100
    p[int(3*len(d)/4)+1] = 100
    p[int(3*len(d)/4)-1] = 100
    q = p

    for i in range(len(d)):
        s.append(s[i] + d[i])

    ax, fx = build_system(d, x)
    mx = solve_system(ax, fx)
    Ax, Bx, Cx, Dx = find_coef(x, mx, d)

    ay, fy = build_system(d, y)
    my = solve_system(ay, fy)
    Ay, By, Cy, Dy = find_coef(y, my, d)

    s_plot = np.linspace(0, s[-1], 1000)

    xs = [spline(s_, Ax, Bx, Cx, Dx) for s_ in s_plot]
    ys = [spline(s_, Ay, By, Cy, Dy) for s_ in s_plot]
    print(ys)

    theta = np.linspace(0, 2 * np.pi, 150)
    a = 1000 * np.cos(theta)
    b = 1000 * np.sin(theta)
    plt.plot(a, b)
    plt.plot(xs, ys)
    plt.show()