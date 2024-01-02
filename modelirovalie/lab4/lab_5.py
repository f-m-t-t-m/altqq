import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt


alphas = np.array([lambda x: x, lambda x: x**3, lambda x: x**5])
betas = np.array([lambda s: 0.6, lambda s: -0.036*s**2, lambda s: 0.000648*s**3])


def f(x):
    return x


def u(x, cs):
    alpha_values = np.array([alpha(x) for alpha in alphas])
    return f(x) + alpha_values.dot(cs)


if __name__ == '__main__':
    fs = np.array([integrate.quad(lambda x: betta(x) * f(x), 0, 1)[0] for betta in betas])
    A = []
    for beta in betas:
        row = [integrate.quad(lambda x: beta(x) * alpha(x), 0, 1)[0] for alpha in alphas]
        A.append(row)
    A = np.array(A)
    A = -1*A
    for i in range(3):
        A[i][i] = 1+A[i][i]

    cs = np.linalg.solve(A, fs)
    interval = np.linspace(0, 1, 11)
    plt.plot(interval, [u(x, cs) for x in interval])
    diff = [u(x, cs) - integrate.quad(lambda s: np.sin(0.6*x*s)/s * u(s, cs), 0, 1)[0] - x for x in interval]
    plt.show()

    plt.plot(interval, diff)
    plt.show()
