import numpy as np


def helper(a: np.ndarray, n: int):
    if n == 0:
        return np.asarray([[1/a[0][0]]])

    a_inv = helper(a, n-1)
    u_n = a[0:n, n].reshape(n, 1)
    v_n = a[n, 0:n].reshape(1, n)
    a_nn = a[n][n]

    alpha_n = a_nn - v_n @ a_inv @ u_n
    p_prev = a_inv + (a_inv @ u_n @ v_n @ a_inv) / alpha_n
    r_n = (-(a_inv @ u_n) / alpha_n).reshape(n, 1)
    q_n = -(v_n @ a_inv / alpha_n).reshape(1, n)

    row1 = np.concatenate((p_prev, r_n), axis=1)
    row2 = np.concatenate((q_n, 1/alpha_n), axis=1)
    return np.concatenate((row1, row2), axis=0)


if __name__ == '__main__':
    a = np.asarray([[5, 1, 3],
                    [3, 6, 3],
                    [0, 2, 3]])
    b = np.asarray([3, 4, 5])

    print(helper(a, 2) @ b)

    print(np.linalg.inv(a) @ b)
