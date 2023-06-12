import numpy as np
from typing import Callable
from matplotlib import pyplot as plt


def left_rectangles(f: Callable, a: float, b: float, n: int, args=()):
    h = (b-a)/n
    res = 0
    for i in range(n):
        res += h * f(a + h*i, *args)
    return res


def fourier_transform(f: Callable, a: float, b: float, m: float, v_n=100, int_n=100):
    vs = np.linspace(0, m, v_n)
    sine = [left_rectangles(lambda t, _v: f(t) * np.sin(_v * t), a, b, int_n, args=(v,)) for v in vs]
    cosine = [left_rectangles(lambda t, _v: f(t) * np.cos(_v * t), a, b, int_n, args=(v,)) for v in vs]
    return vs, sine, cosine


def sine_wave(v):
    return np.sin(4*v)*(-64*np.exp(-16)/(16+v*v) + 8*np.exp(-16)/(16+v*v) + 2*(12*v*v-64)*np.exp(-16)/np.power((16+v*v), 3)) \
        + 2*(48*v - v*v*v)/np.power((16+v*v), 3)


def cosine_wave(v):
    return np.cos(4*v)*(-64*np.exp(-16)/(16+v*v) + 8*np.exp(-16)/(16+v*v) + 2*(12*v*v-64)*np.exp(-16)/np.power((16+v*v), 3)) \
    + np.sin(4*v)*(16*v*np.exp(-16)/(16+v*v) + 64*v*np.exp(-16)/np.power(16+v, 2) + 2*(48*v - v*v*v)*np.exp(-16)/np.power(v*v+16, 3)) \
    + 2*(-12*v*v+64)/np.power(v*v+16, 3)


if __name__ == '__main__':
    vs, sine, cosine = fourier_transform(lambda t: t*t*np.exp(-4*t), 0, 4, 2)
    plt.plot(vs, sine, color='red', label='sine wave')
    plt.plot(vs, cosine, color='blue', label='cosine wave')
    plt.grid(color='grey', linestyle='-')
    plt.legend(loc="upper right")
    plt.show()

    plt.plot(vs, sine_wave(vs), color='red', label='sine wave')
    plt.plot(vs, cosine_wave(vs), color='blue', label='cosine wave')
    plt.grid(color='grey', linestyle='-')
    plt.legend(loc="upper right")
    plt.show()