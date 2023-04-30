from math import factorial
import numpy as np
import matplotlib.pyplot as plt


def plot_triangles(*args: np.ndarray):
    for e in args:
        new_e = np.append(e, [[e[0][0]], [e[1][0]]], axis=1)
        plt.plot(new_e[0], new_e[1])
    plt.savefig("triangles.png")


def calculate_a(e_x: np.ndarray, e_y: np.ndarray, idx: int):
    return e_x[(idx + 1) % 3] * e_y[(idx + 2) % 3] - e_x[(idx + 2) % 3] * e_y[(idx + 1) % 3]


def calculate_b(e_y: np.ndarray, idx: int):
    return e_y[(idx + 1) % 3] - e_y[(idx + 2) % 3]


def calculate_c(e_x: np.ndarray, idx: int):
    return e_x[(idx + 2) % 3] - e_x[(idx + 1) % 3]


def nabla_K1(d: np.ndarray):
    return d.reshape(n_v, 1) @ d.reshape(n_v, 1).T


def len2(i, j):
    if (i == j):
        a = 2
        b = 0
    else:
        a = 1
        b = 1
    return factorial(a) * factorial(b) * l/(1 + a + b)


def len1(a, b):
  return factorial(a)*factorial(b)*l/(factorial(a+b+1))


def get_K2(k):
    K2 = np.array([[len2(i, j) for i in range(n_v)] for j in range(n_v)])
    for i in range(n_v):
        K2[k][i] = 0
        K2[i][k] = 0
    return K2


def sqr(a, b, c):
    return 2*S[0]*factorial(a)*factorial(b)*factorial(c)/factorial(a+b+c+2)


def get_Fv(k):
    Fv = np.array([sqr(1, 0, 0) for i in range(n_v)])
    return Fv


def get_Fs(k):
    Fs = np.array([len1(1, 0) for i in range(n_v)])
    Fs[k] = 0
    return Fs


def get_conn_matrix(k):
    conn = np.zeros((3, 6))
    for i in range(n_v):
        conn[i][int(data[k][i]-1)] = 1
    return conn


if __name__ == '__main__':
    n_v = 3
    n_str = 4
    data = np.loadtxt("data.txt", usecols=(range(3)), ndmin=2)

    l = 2
    h = np.sqrt(l ** 2 - (l / 2) ** 2)
    e_1 = np.array([[0, l / 2, l], [0, h, 0]])
    e_2 = np.array([[l, 3 * l / 2, l / 2], [0, h, h]])
    e_3 = np.array([[l, 2 * l, 3 * l / 2], [0, 0, h]])
    e_4 = np.array([[2 * l, 5 * l / 2, 3 * l / 2], [0, h, h]])
    plot_triangles(e_1, e_2, e_3, e_4)

    e_x = np.concatenate((e_1[0], e_2[0], e_3[0], e_4[0]), axis=0).reshape(n_str, n_v)
    e_y = np.concatenate((e_1[1], e_2[1], e_3[1], e_4[1]), axis=0).reshape(n_str, n_v)

    a = np.array([[calculate_a(e_x[i], e_y[i], j) for j in range(n_v)] for i in range(n_str)])
    b = np.array([[calculate_b(e_y[i], j) for j in range(n_v)] for i in range(n_str)])
    c = np.array([[calculate_c(e_x[i], j) for j in range(n_v)] for i in range(n_str)])
    S = np.array([(a[i][0] + a[i][1] + a[i][2]) / 2 for i in range(n_str)])

    lmb = [1, 2]
    K1 = np.array([(lmb[0]*nabla_K1(b[i]) + lmb[1]*nabla_K1(c[i]))/(4*S[i]) for i in range(n_str)])
    h_list = [1, 0, 1, 1]
    ind_list = [2, 0, 2, 2]
    K2 = np.array([get_K2(ind_list[i]) for i in range(n_str)])
    K = np.array([K1[i] + h_list[i]*K2[i] for i in range(n_str)])

    Q = 3
    q_list = [2, 0, 2, 2]
    T_inf = [0, 0, 0, 0]
    F_v = np.array([get_Fv(i) for i in range(n_str)])
    F_s = np.array([get_Fs(ind_list[i]) for i in range(n_str)])
    F = np.array([-Q*F_v[i] + (h_list[i]*T_inf[i] - q_list[i])*F_s[i] for i in range(n_str)])

    s = np.array([get_conn_matrix(i) for i in range(n_str)])
    A = np.zeros((6, 6))
    B = np.zeros((6,))
    for k in range(n_str):
        A = A + s[k].T @ K[k] @ s[k]
        B = B + s[k].T @ F[k]

    m = [4, 5, 6]
    T_tilde = 2
    for i in m:
        B = B - T_tilde*A.T[i-1]
        B[i-1] = T_tilde
        for j in range(6):
            A[i-1][j] = 0
            A[j][i-1] = 0
        A[i-1][i-1] = 1

    U = np.linalg.inv(A) @ B
    print(U)
