import math

import numpy as np
import enum


class TaskType(enum.Enum):
    direct = 0
    secondary = 1
    dual = 2


def generate_matrices():
    a = np.random.randint(1, 30, (8, 6))
    np.savetxt("a.txt", a, fmt='%d')
    b = np.random.randint(1, 30, (8, 1))
    np.savetxt("b.txt", b, fmt='%d')
    c = np.random.randint(1, 30, (6,))
    np.savetxt("c.txt", c, fmt='%d')
    return a, b, c


def build_matrix_for_direct_task(a, b, c) -> np.ndarray:
    a_c = np.append([-c], a, axis=0)
    eye = np.append([np.zeros(8,)], np.eye(8), axis=0)
    a_c_eye = np.append(a_c, eye, axis=1)
    return np.append(a_c_eye, np.append([[0]], b, axis=0), axis=1)


def build_matrix_for_secondary_task(a, c) -> np.ndarray:
    a = np.append([np.zeros((8,))], a, axis=0)
    minus_i = np.append([np.zeros((6,))], -np.eye(6), axis=0)
    i = np.append([np.ones((6,))], np.eye(6), axis=0)
    c = np.append([[0]], c.reshape((6, 1)), axis=0)
    res = np.hstack([a, minus_i, i, c])
    for i in range(1, len(res)):
        res[0] = res[0] - res[i]
    return res


def build_matrix_for_dual_task(simplex_table: np.ndarray, b) -> np.ndarray:
    base_col = [False for i in range(len(simplex_table[0]))]
    for j in range(len(simplex_table[0])):
        if not math.isclose(simplex_table[0][j], 0, rel_tol=1e-10):
            continue
        is_base_col = True
        for i in range(len(simplex_table)):
            if not (math.isclose(simplex_table[i][j], 0, rel_tol=1e-10) or math.isclose(simplex_table[i][j], 1, rel_tol=1e-10)):
                is_base_col = False
                break
        base_col[j] = is_base_col

    simplex_table = np.delete(simplex_table, np.s_[14:20], axis=1)
    for i in range(len(b)):
        simplex_table[0][i] = b[i]

    for j in range(len(simplex_table[0])):
        if not base_col[j]:
            continue
        for i in range(len(simplex_table)):
            if not math.isclose(simplex_table[i][j], 1, rel_tol=1e-10):
                continue
            simplex_table[0] -= simplex_table[i] * simplex_table[0][j]
            break

    return simplex_table


def simplex(a, b, c, task_type: TaskType):
    if task_type == TaskType.direct:
        simplex_table = build_matrix_for_direct_task(a, b, c)
        y_bias = 0
    elif task_type == TaskType.secondary:
        simplex_table = build_matrix_for_secondary_task(a, c)
        y_bias = 0
    else:
        simplex_table = build_matrix_for_dual_task(a, b)
        y_bias = 1
        print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")

    it = 0
    while True:
        print('------------------------------------------------------------------------')
        for row in list(simplex_table):
            print(list(np.round(row, 2)))

        it += 1
        resolving_column = None
        min_c = 0
        for i in range(len(simplex_table[0])-1):
            if round(simplex_table[0][i], 13) < min_c:
                min_c = simplex_table[0][i]
                resolving_column = i

        if resolving_column is None:
            break

        min_b = float('inf')
        resolving_stroke = None
        for i in range(len(a) - y_bias):
            if 0 < simplex_table[i+1][-1] / simplex_table[i+1][resolving_column] < min_b:
                min_b = simplex_table[i+1][-1] / simplex_table[i+1][resolving_column]
                resolving_stroke = i + 1

        resolving_element = simplex_table[resolving_stroke][resolving_column]
        print(f"Разрешающий столбец:", resolving_column+1)
        print(f"Разрешающая строка:", resolving_stroke+1)
        print(f"Разрешающий элемент:", resolving_element)
        print('------------------------------------------------------------------------')

        simplex_table[resolving_stroke] /= resolving_element

        for i in range(len(simplex_table)):
            if i == resolving_stroke:
                continue
            simplex_table[i] -= simplex_table[i][resolving_column] * simplex_table[resolving_stroke]

    print(it)
    ans = np.zeros(len(simplex_table[0]))
    for j in range(len(simplex_table[0])):
        for i in range(len(simplex_table)):
            if round(simplex_table[i][j], 2) == 1.:
                ans[j] = simplex_table[i][-1]
                break

    return (ans, simplex_table)


if __name__ == '__main__':
    np.printoptions(suppress=True, linewidth=np.inf)
    a = np.loadtxt('a1.txt', usecols=range(6))
    b = np.loadtxt('b1.txt', usecols=range(1), ndmin=2)
    c = np.loadtxt('c1.txt', usecols=range(1))
    res = simplex(a, b, c, TaskType.direct)
    print(np.round(res[0], 2))
    # ans = simplex(res[1], b, [], TaskType.dual)
    # print(np.round(ans[0], 2))
