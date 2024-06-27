import numpy as np
from math import *
from matplotlib import pyplot as plt
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
hyperbola_int = lambda p: (cosh(p)/p - 1/p - sinh(p)/2) / (p**2*sinh(p))

variable_order = lambda t, p: t**(p+3) / (p**2+5*p+6)
variable_order_d = lambda t, p: (p+3)*t**(p+2) / (p**2+5*p+6)
variable_order_d2 = lambda t, p: (p+3)*(p+2)*t**(p+1) / (p**2+5*p+6)
variable_order_int = lambda p: (1/(p+4) - 1/2) * 1/(p**2+5*p+6)


def _calc_M(xs, function, derive, correcting_f, correcting_f_derivative, q):
    h = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    f = [function(x) for x in xs]

    a = np.zeros((len(xs), len(xs)))
    for i in range(1, len(xs) - 1):
        a[i][i - 1] = correcting_f(1, q[i-1]) * h[i - 1]
        a[i][i] = (-correcting_f(1, q[i-1])*h[i-1] - correcting_f(1, q[i])*h[i]
                   + correcting_f_derivative(1, q[i-1])*h[i-1] + correcting_f_derivative(1, q[i])*h[i])
        a[i][i + 1] = correcting_f(1, q[i]) * h[i]

    d = np.zeros(len(xs))
    for i in range(1, len(xs) - 1):
        d[i] = (f[i+1] - f[i])/h[i] - (f[i] - f[i-1])/h[i-1]

    #apply_first_boundary_conditions(a, d, correcting_f, correcting_f_derivative, f, h, q, derive)
    apply_second_boundary_conditions(a, d, correcting_f, correcting_f_derivative, f, h, q, derive)

    return np.linalg.solve(a, d)


def apply_second_boundary_conditions(a, d, correcting_f, correcting_f_derivative, f, h, q, derive):
    a[0][0] = 1
    a[-1][-1] = 1
    d[0] = derive[0]
    d[-1] = derive[1]


def apply_first_boundary_conditions(a, d, correcting_f, correcting_f_derivative, f, h, q, derive):
    a[0][0] = -correcting_f(1, q[0])*h[0] + correcting_f_derivative(1, q[0])*h[0]
    a[0][1] = correcting_f(1, q[0])*h[0]

    a[-1][-2] = correcting_f(1, q[-1])*h[-1]
    a[-1][-1] = -correcting_f(1, q[-1])*h[-1] + correcting_f_derivative(1, q[-1])*h[-1]

    d[0] = (f[1] - f[0])/h[0] - derive[0]
    d[-1] = derive[-1] - (f[-1] - f[-2])/h[0]


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


def derivative_2_M(x, xs, function, d, correcting_f, correcting_f_derivative, correcting_f_derivative_2, q):
    h = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    M = _calc_M(xs, function, d, correcting_f, correcting_f_derivative, q)

    for i in range(len(xs)-1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x-xs[i])/h[i]
            return correcting_f_derivative_2(1-t, q[i])*M[i] + correcting_f_derivative_2(t, q[i])*M[i+1]

def _calc_M_(xs, function, derive, correcting_f, correcting_f_derivative, q):
    h = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    f = [function(x) for x in xs]

    a = np.zeros((len(xs), len(xs)))
    a[0][0] = 1
    for i in range(1, len(xs) - 1):
        a[i][i - 1] = 1/2
        a[i][i] = 2
        a[i][i + 1] = 1/2
    a[-1][-1] = 1

    print(a)

    d = np.zeros(len(xs))
    d[0] = derive[0]
    for i in range(1, len(xs) - 1):
        d[i] = 6/(h[i-1]+h[i]) * ((f[i+1]-f[i])/h[i] - (f[i]-f[i-1])/h[i-1])
    d[-1] = derive[1]

    return np.linalg.solve(a, d)

def derivative_2_M_(x, xs, function, d, correcting_f, correcting_f_derivative, correcting_f_derivative_2, q):
    h = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    M = _calc_M(xs, function, d, correcting_f, correcting_f_derivative, q)
    M = _calc_M_(xs, function, d, correcting_f, correcting_f_derivative, q)

    for i in range(len(xs)-1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x-xs[i])/h[i]
            return (M[i+1] - M[i]) / h[i]


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
