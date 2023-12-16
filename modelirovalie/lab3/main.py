import numpy as np
from typing import Callable, Tuple
import matplotlib.pyplot as plt
from math import cos


def f(x, y):
    return cos(5*x/2 - y/2)


def orig(x):
    return 5*x - 4*np.arctan(np.sqrt(2/3)*np.tan(np.sqrt(3/2)*x))


def euler(f: Callable, point: Tuple[int, int], start: int, finish: int, n: int = 10):
    h = (finish-start)/n
    res = [point]
    for i in range(n):
        res.append((res[i][0]+h, res[i][1]+h*f(res[i][0], res[i][1])))
    return res


def enhanced_euler(f: Callable, point: Tuple[int, int], start: int, finish: int, n: int = 10):
    res = euler(f, point, start, finish, n)
    h = (finish-start)/n
    for i in range(1, len(res)):
        res[i] = (res[i][0], res[i-1][1] + h*(f(res[i-1][0], res[i-1][1])+f(res[i][0], res[i][1]))/2)
    return res


def rk4(f: Callable, point: Tuple[int, int], start: int, finish: int, n: int = 10):
    res = [point]
    h = (finish - start) / n
    for i in range(n):
        k1 = f(res[i][0], res[i][1])
        k2 = f(res[i][0] + h/2, res[i][1] + h*k1/2)
        k3 = f(res[i][0] + h/2, res[i][1] + h*k2/2)
        k4 = f(res[i][0] + h, res[i][1] + h*k3)
        res.append((res[i][0] + h, res[i][1] + h*(k1+2*k2+2*k3+k4)/6))
    return res


def print_table(*arrays):
    str_f = "|{value:^10}|"
    num_f = "|{value:^10.4f}|"
    print(str_f.format(value="x_i") + str_f.format(value="y*_i") +
          str_f.format(value="y_i") + str_f.format(value="y*_i - y_i"))
    for i in zip(*arrays):
        for j in i:
            print(num_f.format(value=j), end='')
        print()


if __name__ == '__main__':
    euler_res = euler(f, (0, 0), 0, 2)
    x = [x[0] for x in euler_res]
    y_euler = [y[1] for y in euler_res]
    y_anal = [orig(i) for i in x]
    euler_error = [np.abs(y_anal[i]-y_euler[i]) for i in range(len(x))]
    plt.plot(x, y_euler, '-o', label='Численное решение', color='blue')
    plt.plot(x, y_anal, '-s', label='Аналитическое решение', color='red')
    plt.legend()
    plt.savefig("euler.png")
    plt.cla()
    plt.plot(x, euler_error, '-s', label='Ошибка', color='red')
    plt.legend()
    plt.savefig("euler-error.png")
    plt.cla()
    print("Euler")
    print_table(x, y_anal, y_euler, euler_error)
    print()

    enhanced_euler_res = enhanced_euler(f, (0, 0), 0, 2)
    y_enhanced_euler = [y[1] for y in enhanced_euler_res]
    enhanced_euler_error = [np.abs(y_anal[i] - y_enhanced_euler[i]) for i in range(len(x))]
    plt.plot(x, y_enhanced_euler, '-o', label='Численное решение', color='blue')
    plt.plot(x, y_anal, '-s', label='Аналитическое решение', color='red')
    plt.legend()
    plt.savefig("euler-enhanced.png")
    plt.cla()
    plt.plot(x, enhanced_euler_error, '-s', label='Ошибка', color='red')
    plt.legend()
    plt.savefig("euler-enhanced-error.png")
    plt.cla()
    print("Enhanced Euler")
    print_table(x, y_anal, y_enhanced_euler, enhanced_euler_error)
    print()

    rk4_res = rk4(f, (0, 0), 0, 2)
    y_rk4 = [y[1] for y in rk4_res]
    rk4_error = [np.abs(y_anal[i] - y_rk4[i]) for i in range(len(x))]
    plt.plot(x, y_rk4, '-o', label='Численное решение', color='blue')
    plt.plot(x, y_anal, '-s', label='Аналитическое решение', color='red')
    plt.legend()
    plt.savefig("rk4.png")
    plt.cla()
    plt.plot(x, rk4_error, '-s', label='Ошибка', color='red')
    plt.legend()
    plt.savefig("rk4-error.png")
    plt.cla()

    plt.plot(x, euler_error, '-o', label='Метод эйлера', color='blue')
    plt.plot(x, enhanced_euler_error, '-*', label='Улучшенный метод эйлера',
             color='green')
    plt.plot(x, rk4_error, '-s', label='Метод Рунге-Кутты 4-го порядка',
             color='red')
    plt.legend()
    plt.savefig("error-union.png")
    plt.cla()
    print("rk_4")
    print_table(x, y_anal, y_rk4, rk4_error)
    print()
    