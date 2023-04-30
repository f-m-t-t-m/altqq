import numpy as np


def generate_matrix():
    matrix = np.random.uniform(0.4, 0.7, (4, 4))
    np.savetxt("a.txt", matrix @ matrix, fmt='%.7f')
    return matrix @ matrix.transpose()


def generate_vector(name: str):
    matrix = np.random.uniform(1, 2, (4, 1))
    np.savetxt(f"{name}.txt", matrix, fmt='%.7f')
    return matrix


def f(x: np.ndarray) -> float:
    res = .5*x.transpose()@A@x + b.transpose()@x
    return res[0][0]


def lagrange_slae(x: np.ndarray) -> np.ndarray:
    return np.append((A + 2*np.eye(4)*y)@x + (b + 2*y*x_0), [[np.linalg.norm(x - x_0)**2 - r**2]], axis=0)


def jacobian(x: np.ndarray) -> np.ndarray:
    J_1_1 = A + 2*np.eye(4)*y
    J_1_2 = 2*(x - x_0)
    J_2_1 = J_1_2.transpose()
    J_2_2 = [[0]]
    J_1 = np.append(J_1_1, J_1_2, axis=1)
    J_2 = np.append(J_2_1, J_2_2, axis=1)
    return np.append(J_1, J_2, axis=0)


def newton(x_k: np.ndarray, epsilon=1e-6, max_iter=30):
    x_prev = x_k
    x_cur = x_prev - np.linalg.inv(jacobian(x_prev[0:-1])) @ lagrange_slae(x_prev[0:-1])
    it = 0
    while np.linalg.norm(x_cur[0:-1] - x_prev[0:-1]) > epsilon and it < max_iter:
        it += 1
        x_prev = x_cur
        x_cur = x_prev - np.linalg.inv(jacobian(x_prev[0:-1])) @ lagrange_slae(x_prev[0:-1])
    return x_cur


if __name__ == '__main__':
    A = generate_matrix()
    print(A)
    #A = np.loadtxt("a.txt", usecols=(range(4)))
    b = np.loadtxt("b.txt", usecols=(range(1)), ndmin=2)
    x_0 = np.loadtxt("x_0.txt", usecols=(range(1)), ndmin=2)
    r = 5
    a = 4
    y = 3
    sign = 1
    x_ = np.append(x_0, [[y]], axis=0)

    print("------------------------------------------------------")
    x_star = -np.linalg.inv(A) @ b
    f_in_x_star = f(x_star)
    print(f"x* =\n{x_star}")
    print(f"function in x* = {f_in_x_star}")
    print(f"x*-x_0 =\n{x_star - x_0}")
    print(f"||x*-x_0|| = {np.linalg.norm(x_star -  x_0)}")
    print("------------------------------------------------------")

    for i in range(8):
        sign = -sign
        x_k = x_.copy()
        x_k[i//2][0] += sign * a
        print("------------------------------------------------------")
        print(f"first approach {i+1}:\n{x_k[0:-1]}")
        res = newton(x_k)
        print("result x")
        print(res[0:-1])
        print(f"result y = {res[4][0]}")
        print(f"function result = {f(res[0:-1])}")
        print("------------------------------------------------------")
