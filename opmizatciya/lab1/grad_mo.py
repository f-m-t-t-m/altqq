import numpy as np
from matplotlib import pyplot as plt

EPSILON = 1e-05

H = 1e-04

A = np.array([
    [2, 1, 1, 1, 1, 1],
    [1, 2, 1, 1, 1, 1],
    [1, 1, 2, 1, 1, 1],
    [1, 1, 1, 2, 1, 1],
    [1, 1, 1, 1, 2, 1],
    [2, 1, 1, 1, 1, 2],
])

B = np.array([1, 1, 1, 1, 1, 1])
X_0 = np.array([1, 1, 1, 1, 1, 1])


def gen_positive_matrix(n: int) -> np.ndarray:
    bb = np.random.rand(n, n)
    return np.dot(bb, bb.T)


def is_positively_defined(a: np.ndarray) -> bool:
    vals = np.linalg.eig(a)[0]
    print(vals)
    for e in vals:
        if e <= 0:
            return False
    return True


def base_function(x: np.ndarray, a: np.ndarray, b: np.ndarray):
    left = x.T.dot(a).dot(x) / 2
    right = x.dot(b)
    return left + right


def derivative_function(x: np.ndarray, a: np.ndarray, b: np.ndarray):
    left = np.dot((a.T + a), x)
    left = np.dot(left, 0.5)
    return left + b


def gradient_descent(a: np.ndarray, b: np.ndarray, x_0: np.ndarray, is_logging=True) -> \
        tuple[list[np.ndarray], int]:
    count = 1
    vectors = [np.array(x_0)]
    if is_logging:
        print(vectors[0])
    while True:
        count += 1
        vectors.append(vectors[-1] - np.dot(derivative_function(vectors[-1], a, b), H))
        if is_logging:
            print(vectors[-1])
        if np.linalg.norm(vectors[-1] - vectors[-2]) < EPSILON:
            return vectors, count


def exact_val(a: np.ndarray, b: np.ndarray):
    left = np.dot((a.T + a), 0.5)
    return np.linalg.solve(left, -b)


exact = exact_val(A, B)

print(A)
print(is_positively_defined(A))
print()

result = gradient_descent(A, B, X_0)
print('exact value: ', exact_val(A, B))
print('count: ', result[1])

print('промежуточные значения')
print(result[0][len(result[0]) // 4])
print(result[0][len(result[0]) // 2])
print(result[0][3 * len(result[0]) // 4])
print(result[0][len(result[0]) - 1])

print('промежуточные значения функции')
print(base_function(result[0][len(result[0]) // 4], A, B))
print(base_function(result[0][len(result[0]) // 2], A, B))
print(base_function(result[0][3 * len(result[0]) // 4], A, B))
print(base_function(result[0][len(result[0]) - 1], A, B))

print('погрешность')
for i in range(0, 6):
    print(abs(result[0][len(result[0]) - 1][i] - exact[i]))
print(base_function(result[0][len(result[0]) - 1] - exact, A, B))
print('Точное значение:', base_function(exact, A, B))

func_val = [base_function(x_i, A, B) for x_i in result[0]]
plt.plot(np.linspace(0, len(result[0]) - 1, len(result[0])), func_val)
plt.xlabel('кол-во итераций')
plt.ylabel('значение')
plt.grid(True)
plt.show()
