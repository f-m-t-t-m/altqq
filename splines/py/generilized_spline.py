import math

import numpy as np
import matplotlib.pyplot as plt
from math import *
from scipy import integrate

from functions import *


rational = lambda t, p: t ** 3 / (1 + p * (1 - t)) * 1 / (6 + 6 * p + 2 * p ** 2)
rational_d = lambda t, p: (3 * t ** 2 * (1 + p * (1 - t)) + p * t ** 3) / (1 + p * (1 - t)) ** 2 * 1 / (6 + 6 * p + 2 * p ** 2)
rational_d2 = lambda t, p: ((6*t+6*p*t-6*p*t**2)*(1+p*(1-t))**2 + 2*(3*t**2+3*p*t**2-2*p*t**3)*(1+p*(1-t))*p) / (1+p*(1-t))**4 * 1 / (6 + 6 * p + 2 * p ** 2)
rational_int = lambda p: ((6*p**3 + 18*p**2 + 18*p + 6) * math.log(p+1)/(6*p**4) - 11/(6*p) - 5/(2*p**2) - 1/p**3 - 1/2) * 1 / (6 + 6 * p + 2 * p ** 2)

exponent = lambda t, p: t**3*e**(-p*(1-t)) / (6+6*p+p**2)
exponent_d = lambda t, p: ((3*t**2 + p*t**3)*e**(-p*(1-t))) / (6+6*p+p**2)
exponent_d2 = lambda t, p: ((6*t + 6*p*t**2 + p**2*t**3)*e**(-p*(1-t))) / (6+6*p+p**2)
exponent_int = lambda p: (6/(p**4*e**p) + 1/p - 3/p**2 + 6/p**3 - 6/p**4 - 1/2) / (6+6*p+p**2)

hyperbola = lambda t, p: (sinh(p*t)-p*t)/(p**2*sinh(p))
hyperbola_d = lambda t, p: (p*cosh(p*t)-p)/(p**2*sinh(p))
hyperbola_d_2 = lambda t, p: (p**2*sinh(p*t))/(p**2*sinh(p))
hyperbola_int = lambda p: (cosh(p)/p - p/2 - 1/p - 1/2*(sinh(p)-p)) / (p**2*sinh(p))

variable_order = lambda t, p: t**(p+3) / (p**2+5*p+6)
variable_order_d = lambda t, p: (p+3)*t**(p+2) / (p**2+5*p+6)
variable_order_d2 = lambda t, p: (p+3)*(p+2)*t**(p+1) / (p**2+5*p+6)
variable_order_int = lambda p: (1/(p+4) - 1/2) * 1/(p**2+5*p+6)


def _calc_M(xs, function, derive, correcting_f, correcting_f_derivative, q):
    h = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    f = [function(x) for x in xs]

    a = np.zeros((len(xs), len(xs)))
    a[0][0] = 1
    for i in range(1, len(xs) - 1):
        a[i][i - 1] = correcting_f(1, q[i-1]) * h[i - 1]
        a[i][i] = (- correcting_f(1, q[i-1])*h[i-1] - correcting_f(1, q[i])*h[i]
                   + correcting_f_derivative(1, q[i-1])*h[i-1] + correcting_f_derivative(1, q[i])*h[i])
        a[i][i + 1] = correcting_f(1, q[i]) * h[i]
    a[-1][-1] = 1

    d = np.zeros(len(xs))
    d[0] = derive[0]
    for i in range(1, len(xs) - 1):
        d[i] = (f[i+1] - f[i])/h[i] - (f[i] - f[i-1])/h[i-1]
    d[-1] = derive[1]

    return np.linalg.solve(a, d)


def spline_M(x, xs, function, d, correcting_f, correcting_f_derivative, q):
    h = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    f = [function(x) for x in xs]
    M = _calc_M(xs, function, d, correcting_f, correcting_f_derivative, q)

    for i in range(len(xs)-1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x-xs[i])/h[i]
            return ((f[i] - correcting_f(1, q[i]) * M[i] * h[i] ** 2) * (1 - t)
                    + (f[i+1] - correcting_f(1, q[i]) * M[i + 1] * h[i] ** 2) * t
                    + correcting_f(1 - t, q[i]) * M[i] * h[i] ** 2
                    + correcting_f(t, q[i]) * M[i + 1] * h[i] ** 2)


def derivative_1_M(x, xs, function, d, correcting_f, correcting_f_derivative, q):
    h = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    f = [function(x) for x in xs]
    M = _calc_M(xs, function, d, correcting_f, correcting_f_derivative, q)

    for i in range(len(xs)-1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x-xs[i])/h[i]
            return (-(f[i] - correcting_f(1, q[i])*M[i]*h[i]**2)/h[i]
                    + (f[i+1] - correcting_f(1, q[i])*M[i+1]*h[i]**2)/h[i]
                    - correcting_f_derivative(1-t, q[i])*M[i]*h[i]
                    + correcting_f_derivative(t, q[i])*M[i+1]*h[i])


def derivative_2_M(x, xs, function, d, correcting_f, correcting_f_derivative, q):
    h = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    M = _calc_M(xs, function, d, correcting_f, correcting_f_derivative, q)

    for i in range(len(xs)-1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x-xs[i])/h[i]
            return correcting_f_derivative(1-t, q[i])*M[i] + correcting_f_derivative(t, q[i])*M[i+1]


def int_M(xs, function, d, correcting_f, correcting_f_derivative, correcting_f_int, q):
    h = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    f = [function(x) for x in xs]
    M = _calc_M(xs, function, d, correcting_f, correcting_f_derivative, q)

    sum = 0
    for i in range(len(xs)-1):
        sum += 1/2*h[i]*f[i] + 1/2*h[i]*f[i+1] + correcting_f_int(q[i])*h[i]**3*(M[i] + M[i+1])
    return sum


def norm(val1, val2):
    np1, np2 = np.asarray(val1), np.asarray(val2)
    np3 = np.absolute(np.subtract(np1, np2))
    return np3.max()


if __name__ == '__main__':
    xs = np.linspace(0, 1, 2000)
    xs_ = np.linspace(0, 1, 11)
    q = [0] * len(xs_)
    q1 = [1]*len(xs_)
    der = [derives2[1](xs_[0]), derives2[1](xs_[-1])]
    experiments = [
        (rational, rational_d, rational_d2, q, 'Кубический сплайн'),
        (rational, rational_d, rational_d2, q[:8] + [10, 5.49] + q[10:], 'Рациональный сплайн'),
        (exponent, exponent_d, exponent_d2, q[:8] + [10, 7.2] + q[10:], 'Экспоненциальный сплайн'),
        (hyperbola, hyperbola_d, hyperbola_d_2, q1[:8] + [10, 10] + q1[10:], 'Гиперболический сплайн'),
        (variable_order, variable_order_d, variable_order_d2,  q[:8] + [10, 7.6] + q[10:], 'Сплайн переменного порядка')]

    for c_f, c_d, c_d_2, q, title in experiments:
        #ys_spline = [spline_M(x, xs_, functions[1], der, c_f, c_d, q) for x in xs]
        #ys_spline = [derivative_1_M(x, xs_, functions[1], der, c_f, c_d, q) for x in xs]
        ys_spline = [derivative_2_M(x, xs_, functions[1], der, c_f, c_d_2, q) for x in xs]
        #ys3 = [functions[1](x) for x in xs]
        #ys3 = [derives[1](x) for x in xs]
        ys3 = [derives2[1](x) for x in xs]
        #dots = [functions[1](x) for x in xs_]

        print(title + ': ' + repr(norm(ys3, ys_spline)))

        #plt.scatter(xs_, dots, 20)
        plt.plot(xs, ys_spline, 'b')
        plt.plot(xs, ys3, 'r--')
        plt.title(title)
        plt.show()

    experiments = [
        (rational, rational_d, rational_d2, rational_int, q1),
        (rational, rational_d, rational_d2, rational_int, q1[:8] + [10, 5.49] + q1[10:]),
        (exponent, exponent_d, exponent_d2, exponent_int, q1[:8] + [10, 7.2] + q1[10:]),
        (hyperbola, hyperbola_d, hyperbola_d_2, hyperbola_int, q1[:8] + [10, 10] + q1[10:]),
        (variable_order, variable_order_d, variable_order_d2, variable_order_int, q[:8] + [10, 7.6] + q[10:])]

    int = integrate.quad(functions[1], 0, 1)[0]
    print(int)
    for c_f, c_d, c_d_2, c_int, q in experiments:
        print(int_M(xs_, functions[1], der, c_f, c_d, c_int, q))
        print(abs(int - int_M(xs_, functions[1], der, c_f, c_d, c_int, q)))



