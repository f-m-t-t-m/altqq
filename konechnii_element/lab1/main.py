from math import *
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt


N = 10


def a(x, i, j):
    return j*i*pi**2*cos(i*pi*x)*cos(j*pi*x)*e**x + sin(i*pi*x)*sin(j*pi*x)


def integrate_a(i, j):
    return integrate.quad(a, 0, 1, args=(i+1, j+1))[0]


def g(x, j):
    return (e**x + 1)*sin(j*pi*x)


def integrate_g(j):
    return integrate.quad(g, 0, 1, args=(j+1))[0]


def f(x, j):
    return (x**2 - 2*x*e**x - x - e**x)*sin(j*pi*x)


def integrate_f(j):
    return integrate.quad(f, 0, 1, args=(j+1))[0]


def make_matrix(n: int) -> np.matrix:
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i][j] = integrate_a(i, j)
    return np.matrix(matrix)


def make_vector(n: int) -> np.matrix:
    vector = np.zeros((n, 1))
    for i in range(n):
        vector[i][0] = integrate_f(i)
    return np.matrix(vector)


def u(x):
    res = 0
    for idx, coord in np.ndenumerate(vectorC):
        res += coord*sin((idx[0] + 1)*pi*x)
    return res


if __name__ == '__main__':
    matrixA = make_matrix(N)
    vectorG = make_vector(N)
    vectorC = np.linalg.inv(matrixA) @ vectorG
    np.set_printoptions(suppress=True)
    # print(vectorC)
    xs = np.linspace(0, 1, 10)
    u_values = [round(u(x), 7) for x in xs]
    print(u_values)
    plt.plot(xs, u_values)
    u_exact = lambda x: x**2 - x
    u_exact_values = [round(u_exact(x), 7) for x in xs]
    print(u_exact_values)
    # plt.plot(xs, u_exact_values)
    plt.savefig("test.png")
