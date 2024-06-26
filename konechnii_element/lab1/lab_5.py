import math

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt


def K(x, s):
    return (1+s)*(np.e**(0.2*x*s)-1)


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


def f(x):
    return 1/x


def u(x, cs, alphas):
    alpha_values = np.array([alpha(x) for alpha in alphas])
    return f(x) + alpha_values.dot(cs)


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


if __name__ == '__main__':
    alphas1 = np.array([lambda x: x, lambda x: x ** 2, lambda x: x ** 3])
    betas1 = np.array([lambda s: 0.2*(s+s**2), lambda s: 0.02*(s**2+s**3), lambda s: 0.0013*(s**3+s**4)])

    alphas = lagrange()[0]
    betas = lagrange()[1]
    cs = solve_system(alphas, betas)
    cs1 = solve_system(alphas1, betas1)

    interval = np.linspace(0, 1, 11)

    figure, axis = plt.subplots(2)
    figure.tight_layout(pad=1.0)

    axis[0].plot(interval, [u(x, cs, alphas) for x in interval], 'b')
    axis[0].set_title("Аппроксимация ядра многочленом Лагранжа")

    axis[1].plot(interval, [u(x, cs1, alphas1) for x in interval], 'b')
    axis[1].set_title("Аппроксимация ядра рядом Тейлора")
    plt.show()

    for i in range(11):
        print(interval[i], end=' ')
        print(u(interval[i], cs, alphas), end=' ')
        print(u(interval[i], cs1, alphas1))
        print("---------")
