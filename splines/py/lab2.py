import numpy as np
import matplotlib.pyplot as plt
import math


def function(x):
    return math.cos(math.pi * x**2/2)


def function_deriv(x):
    return -math.pi*x*math.sin(math.pi*x**2/2)


def spline(x):
    for i in range(len(spline_xs)-1):
        if spline_xs[i] <= x <= spline_xs[i + 1]:
            t = (x-spline_xs[i])/hs[i]
            return (1 - t) * exact_values[i] + t * exact_values[i + 1] - t * (1 - t) / 6 * hs[i] ** 2 * (
                        (2 - t) * momenti[i] + (1 + t) * momenti[i + 1])


def spline_int():
    res = 0
    for i in range(len(spline_xs)-1):
        res += 1/2*hs[i]*(exact_values[i] + exact_values[i+1]) - 1/24*hs[i]**3*(momenti[i] + momenti[i+1])
    return res


def calc_mu(hs: list):
    return [0] + [hs[i-1] / (hs[i-1]+hs[i]) for i in range(1, len(hs))]


def build_system(xs: np.array):
    a = np.zeros((len(xs), len(xs)))
    a[0][0] = 2
    a[0][1] = 1

    for i in range(1, len(xs)-1):
        a[i][i-1] = mus[i] * (1 - epsilons[i]**2/hs[i-1]**2)
        a[i][i] = 2 + epsilons[i]**2/(hs[i-1] * hs[i])
        a[i][i+1] = lambdas[i] * (1 - epsilons[i]**2/hs[i]**2)

    a[-1][-2] = 1
    a[-1][-1] = 2

    f = np.zeros(len(xs))
    f[0] = -6/hs[0] * (function_deriv(xs[0]) - (exact_values[1] - exact_values[0])/hs[0])

    for i in range(1, len(xs)-1):
        f[i] = 6/(hs[i-1] + hs[i])*((exact_values[i+1] - exact_values[i])/hs[i] - (exact_values[i] - exact_values[i-1])/hs[i-1])

    f[-1] = 6/hs[-2] * (function_deriv(xs[-1]) - (exact_values[-1] - exact_values[-2])/hs[-2])

    return a, f


if __name__ == '__main__':
    spline_xs = np.linspace(0, 0.2, 4)
    hs = [spline_xs[i+1] - spline_xs[i] for i in range(len(spline_xs)-1)]
    epsilons = [0 for i in range(len(spline_xs)-1)]
    mus = calc_mu(hs)
    lambdas = [1 - mu for mu in mus]
    exact_values = [function(x) for x in spline_xs]
    a, f = build_system(spline_xs)
    momenti = np.linalg.solve(a, f)
    print(momenti)

    print(spline_int())
    print(0.2 - 0.2**5/10 + 0.2**9/216)

    xs = np.linspace(0, 0.2, 100)
    ys = [function(x) for x in xs]
    plt.plot(xs, ys, 'r')

    spline_ys = [spline(x) for x in xs]
    plt.plot(xs, spline_ys, 'b')

    plt.show()

