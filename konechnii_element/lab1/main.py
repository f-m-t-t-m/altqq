import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return 1 - x/2 + 0.325* (x**2-x)


def print_table(*arrays):
    str_f = "|{value:^10}|"
    num_f = "|{value:^10.5f}|"
    print(str_f.format(value="x_i") + str_f.format(value="y*_i") +
          str_f.format(value="y_i") + str_f.format(value="y*_i - y_i"))
    for i in zip(*arrays):
        for j in i:
            print(num_f.format(value=j), end='')
        print()


if __name__ == '__main__':
    interval = np.linspace(0, 1, 10)
    ys_anal = [1/(x+1) for x in interval]
    ys_comp = [f(x) for x in interval]
    diff = [abs(f(x) - 1/(x+1)) for x in interval]
    print_table(interval, ys_anal, ys_comp, diff)

    plt.plot(interval, [1/(x+1) for x in interval], label='Точное решение')
    plt.plot(interval, [f(x) for x in interval], label='Аналитическое решение')
    plt.legend()
    plt.savefig("plot.png")

