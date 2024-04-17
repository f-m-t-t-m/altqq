import math

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt


def K(x, s):
    return (1+s)*(np.e**(0.2*x*s)-1)


def f(x):
    return 1/x


def lagrange():
    interval = np.linspace(0, 1, 3)
    betas = []
    alphas = []
    numerators = []
    for i in range(len(interval)):
        denominator = 1
        numerators.append([lambda x: 1])
        for j in range(len(interval)):
            if i == j:
                continue
            numerators[i].append(lambda z, bound_j=j: z-interval[bound_j])
            denominator *= (interval[i] - interval[j])

        alphas.append(lambda p, bound_i=i, bound_den=denominator: (math.prod(num(p) for num in numerators[bound_i]) /
                                                                       bound_den))
        betas.append(lambda s, bound_i=i: K(interval[bound_i], s))
    return alphas, betas


def solve_system(alphas, betas):
    fs = np.array([integrate.quad(lambda x: beta(x) * f(x), 0, 1)[0] for beta in betas])
    A = []
    for beta in betas:
        row = [integrate.quad(lambda x: beta(x) * alpha(x), 0, 1)[0] for alpha in alphas]
        A.append(row)
    A = np.array(A)
    A = -1*A
    for i in range(len(betas)):
        A[i][i] = 1+A[i][i]

    return np.linalg.solve(A, fs)


def u(x, cs, alphas):
    alpha_values = np.array([alpha(x) for alpha in alphas])
    return f(x) + alpha_values.dot(cs)
