import numpy as np
import matplotlib.pyplot as plt

h = 0.1

def A_k(x):
    return 1/(3*h) * (1 + (1+x)*h/2 - h**2/6)


def D_k(x):
    return 1/(3*h) * (1 - (1+x)*h/2 - h**2/6)


def C_k(x):
    return -A_k(x) - D_k(x) - 2*h/6


def F_k(x):
    return 2*h/6 * 2/(x+1)**3


def print_table(*arrays):
    str_f = "|{value:^10}|"
    num_f = "|{value:^10.5f}|"
    print(str_f.format(value="x_i") + str_f.format(value="y*_i") +
          str_f.format(value="b_i") + str_f.format(value="y*_i - b_i"))
    for i in zip(*arrays):
        for j in i:
            print(num_f.format(value=j), end='')
        print()


if __name__ == '__main__':
    interval = np.linspace(0, 1, 11)
    ys_anal = [1/(x+1) for x in interval]
    matrix = np.zeros((11, 11))
    matrix[0][0] = -20.66666
    matrix[0][1] = -0.333333
    for i in range(1, 10):
        matrix[i][i-1] = A_k(interval[i])
        matrix[i][i] = C_k(interval[i])
        matrix[i][i+1] = D_k(interval[i])
    matrix[10][9] = 0.66666
    matrix[10][10] = -18.66666

    F = np.zeros(11)
    F[0] = -20.9
    for i in range(1, 10):
        F[i] = F_k(interval[i])
    F[10] = -8.975

    b = np.linalg.solve(matrix, F)
    print(b.tolist())
    print(ys_anal)
    plt.plot(interval, ys_anal)
    plt.plot(interval, b)
    plt.show()

    diff = [abs(ys_anal[i] - b.tolist()[i]) for i in range(11)]
    print_table(interval, ys_anal, b, diff)

    plt.plot(interval, diff)
    plt.show()

