import numpy as np


def fadeev(matrix: np.ndarray):
    polynom_coefficients = [1]
    n = matrix.shape[0]
    B = [np.eye(n)]
    for i in range(n):
        A = matrix @ B[-1]
        polynom_coefficients.append(-np.trace(A) / (i+1))
        B.append(A + polynom_coefficients[-1]*np.eye(n))
    polynom_coefficients = [(-1)**n * x for x in polynom_coefficients]

    return polynom_coefficients, B


if __name__ == '__main__':
    A = np.asarray([[2, 1, 1],
                    [1, 2.5, 1],
                    [1, 1, 3]])

    fadeev_res = fadeev(A)
    eigvals = np.roots(fadeev_res[0])
    print(eigvals)

    n = A.shape[0]

    eigvecs = []
    for i in range(n):
        res = np.zeros(A.shape)
        for j in range(n):
            res += eigvals[i]**(n-j-1)*fadeev_res[1][j]
        eigvecs.append(res[:,0]/np.linalg.norm(res[:,0], ord=1))

    for i in range(n):
        print('-------------------------------------------------------------------------')
        print(f'Собственное число = {eigvals[i]}')
        print(f'Собственный вектор = {eigvecs[i]}')
        print(f'A*u = {A @ eigvecs[i]}')
        print(f'lambda*u = {eigvecs[i]*eigvals[i]}')