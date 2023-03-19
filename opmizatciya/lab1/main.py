import numpy as np
import matplotlib.pyplot as plt


def generate_pd_matrix(n: int, m: int) -> np.ndarray:
    matrix = np.random.uniform(0.5, 1, (n, m))
    return np.matmul(matrix, matrix.transpose())


def f(x: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return .5 * x.transpose() @ a @ x + b.transpose() @ x


def f_derivative(a: np.ndarray, b: np.ndarray, x: np.ndarray) -> np.ndarray:
    return .5 * np.matmul(np.add(a.transpose(), a), x) + b


def gradient_descent(a: np.ndarray, b: np.ndarray, initial_x: np.ndarray, h=10e-4, precision=10e-5):
    counter = 0
    res_tuples = []
    error = float('inf')
    prev = None
    current = initial_x
    while error >= precision:
        prev = current
        current = np.subtract(prev, h * f_derivative(a, b, prev))
        error = np.linalg.norm(np.subtract(current, prev), 'fro')
        counter += 1
        res_tuples.append((counter, current))
    return res_tuples


if __name__ == '__main__':
    matrix_a = np.loadtxt("matrix_a.txt", usecols=range(6))
    vector_b = np.loadtxt("vector_b.txt", usecols=range(1), ndmin=2)
    x_sol = np.linalg.solve(.5 * np.add(matrix_a.transpose(), matrix_a), -vector_b)
    vector_x0 = x_sol * -2

    ans = gradient_descent(matrix_a, vector_b, vector_x0)
    #print(len(ans))
    #print(ans[int(len(ans)/4)][1])
    #print(ans[int(len(ans)/2)][1])
    #print(ans[3 * int(len(ans) / 4)][1])
    #print(ans[len(ans) - 1][1])
    # print(vector_x0)
    # print(x_sol)

    #print(f(ans[int(len(ans)/4)][1], matrix_a, vector_b))
    #print(f(ans[int(len(ans) / 2)][1], matrix_a, vector_b))
    #print(f(ans[3 * int(len(ans) / 4)][1], matrix_a, vector_b))
    #print(f(ans[int(len(ans)) - 1][1], matrix_a, vector_b))
    #
    #print(f(x_sol, matrix_a, vector_b))
    print(np.linalg.eigvals(matrix_a))

    f_values = np.ravel([f(i[1], matrix_a, vector_b).flatten() for i in ans]).tolist()
    plt.plot([i[0] for i in ans], f_values, 'black')
    plt.savefig('fig1.png')
