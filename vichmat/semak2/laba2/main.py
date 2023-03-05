import numpy as np
import matplotlib.pyplot as plt

N = 10
START = 0
END = 1.1
STEP = .1


def build_hilbert_matrix(epsilon):
    hilbert_matrix = [[(1 / (i + j + 1) + N*epsilon) for j in range(N)] for i in range(N)]
    return np.matrix(hilbert_matrix)


def get_conds():
    epsilons = np.arange(START, END, STEP)
    return [np.linalg.cond(build_hilbert_matrix(epsilon)) for epsilon in epsilons]


if __name__ == '__main__':
    epsilons = np.arange(START, END, STEP)
    conds = get_conds()
    print(conds)
    plt.plot(epsilons, conds, marker='o')
    plt.ticklabel_format(useOffset=False)
    plt.xlabel('$\epsilon$')
    plt.ylabel('$\mu$')
    plt.savefig('1.jpg')
