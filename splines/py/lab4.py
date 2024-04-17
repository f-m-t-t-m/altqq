import numpy as np
import matplotlib.pyplot as plt

n = 10
h = 1/n
print(h)

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
    interval = np.linspace(0, 1, n+1)
    ys_anal = [1/(x+1) for x in interval]
    matrix = np.zeros((n+1, n+1))

    matrix[0][0] = C_k(0) - 4*h*A_k(0)/h
    matrix[0][1] = D_k(0) - h*A_k(0)/h
    for i in range(1, n):
        matrix[i][i-1] = A_k(interval[i])
        matrix[i][i] = C_k(interval[i])
        matrix[i][i+1] = D_k(interval[i])
    matrix[n][n-1] = A_k(1) - h*D_k(1)/h
    matrix[n][n] = C_k(1) - 4*h*D_k(1)/h

    F = np.zeros(n+1)
    F[0] = F_k(0) - 6*1*h*A_k(0)/h
    for i in range(1, n):
        F[i] = F_k(interval[i])
    F[n] = F_k(1) - 6*0.5*h*D_k(1)/h

    b = np.linalg.solve(matrix, F)
    plt.plot(interval, ys_anal)
    plt.plot(interval, b)
    plt.show()

    diff = [abs(ys_anal[i] - b.tolist()[i]) for i in range(n+1)]
    print_table(interval, ys_anal, b, diff)
