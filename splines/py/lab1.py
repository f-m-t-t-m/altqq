import math
import numpy as np


def function(x, alpha):
    return alpha/(1+9*x**2)


def function_deriv(x, alpha):
    return -alpha * 18*x/(1 + 9*x**2)**2


def calc_mu(hs: list):
    return [0] + [hs[i-1] / (hs[i-1]+hs[i]) for i in range(1, len(hs))]


def build_system(xs: np.array, alpha: int):
    a = np.zeros((len(xs), len(xs)))
    a[0][0] = 1

    for i in range(1, len(xs)-1):
        a[i][i-1] = lambdas[i]
        a[i][i] = 2
        a[i][i+1] = mus[i]

    a[len(xs)-1][len(xs)-1] = 1

    f = np.zeros(len(xs))
    f[0] = function_deriv(xs[0], alpha) - 0.5

    for i in range(1, len(xs)-1):
        f[i] = 3 * (mus[i] * (exact_values[i+1] - exact_values[i]) / hs[i] + lambdas[i] * (exact_values[i] - exact_values[i-1]) / hs[i-1])

    f[len(xs)-1] = function_deriv(xs[-1], alpha) - 0.5

    return a, f


if __name__ == '__main__':
    alpha = 2
    xs = np.linspace(-1, 1, 5)
    hs = [xs[i+1] - xs[i] for i in range(len(xs)-1)]
    mus = calc_mu(hs)
    lambdas = [1 - mu for mu in mus]
    exact_values = [function(x, alpha) for x in xs]
    a, f = build_system(xs, alpha)
    nakloni = np.linalg.solve(a, f)
    print(nakloni)



    spline_values = []
    for i in range(len(xs)-1):
        t = 0.5
        spline_values.append((1-3*t**2+2*t**3) * exact_values[i] + (3*t**2-2*t**3) * exact_values[i+1]
                             + (1-t)**2 * nakloni[i] * hs[i] * t - (1-t)*nakloni[i+1] * hs[i] * t**2)

    exact_values_in_midpoints = [function((xs[i - 1] + xs[i]) / 2, alpha) for i in range(1, len(xs))]

    print([(xs[i-1] + xs[i])/2 for i in range(1, len(xs))])
    print(exact_values_in_midpoints)
    print(spline_values)
    print([abs(exact_values_in_midpoints[i] - spline_values[i]) for i in range(len(spline_values))])