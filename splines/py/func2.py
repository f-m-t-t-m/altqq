from generilized_spline import *
from generilized_spline import _calc_M


def cos_int(alpha, M, h, x, f):
    ret = 0
    for i in range(len(M)-1):
        ret += (cos(alpha*x[i+1]) - cos(alpha*x[i]))/h[i] * (M[i+1] - M[i])
    ret *= -1/alpha**4

    A = (-(f[1] - f[0])/h[0] + h[0]/6 * (2*M[0] + M[1])) * 1/alpha**2
    ret += A*cos(alpha*x[0])
    C = (f[0] - 1/alpha**2 * M[0])*1/alpha
    ret -= C*sin(alpha*x[0])

    B = (-(f[-1] - f[-2]) / h[-1] + h[-1] / 6 * (2 * M[-1] + M[-2])) * 1 / alpha ** 2
    ret += B*cos(alpha*x[-1])
    D = (-f[-1] + 1 / alpha ** 2 * M[0]) * 1 / alpha
    ret -= D*sin(alpha*x[-1])
    return ret


if __name__ == '__main__':
    xs = np.linspace(0, 9*pi/20, 1000)
    xs_ = np.linspace(0, 9*pi/20, 14)
    #xs_ = np.append(xs_, [0.1077, 0.3644, 0.6578, 0.963, 1.272])
    xs_.sort()

    q = [0] * len(xs_)
    q1 = [1]* len(xs_)
    der = [derives2[2](0), derives2[2](9*pi/20)]
    x_table = [0.1, 0.2, 0.4, 0.6, 1, 1.2, 1.5]
    experiments = [
        (rational, rational_d, rational_d2, q, 'Кубический сплайн')]

    for c_f, c_d, c_d_2, q, title in experiments:
        ys_spline = [spline_M(x, xs_, functions[2], der, c_f, c_d, q) for x in xs]
        #ys_spline = [derivative_1_M(x, xs_, functions[2], der, c_f, c_d, q) for x in xs]
        #ys_spline = [derivative_2_M(x, xs_, functions[2], der, c_f, c_d, c_d_2, q) for x in xs]
        ys3 = [functions[2](x) for x in xs]
        #ys3 = [derives[2](x) for x in xs]
        #ys3 = [derives2[2](x) for x in xs]

        # print(title + ': ' + repr(norm(ys3, ys_spline)))
        # for x in x_table:
        #     print(functions[2](x), end=' ')
        #     print(spline_M(x, xs_, functions[2], der, c_f, c_d, q), end=' ')
        #     print((spline_M(x, xs_, functions[2], der, c_f, c_d, q) - functions[2](x)).__abs__())
        plt.plot(xs, ys_spline, 'b')
        plt.plot(xs, ys3, 'r--')
        plt.title(title)
        plt.show()

    # experiments = [
    #     (rational, rational_d, rational_d2, rational_int, q)]
    #
    # int = integrate.quad(functions[2], 0, 9*pi/20)[0]
    # print(int)
    # for c_f, c_d, c_d_2, c_int, q in experiments:
    #     M = _calc_M(xs_, lambda x: x**2, [2, 2], rational, rational_d, q)
    #     h = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    #     f = [x**2 for x in xs]
    #     print(int - cos_int(10, M, h, xs_, f))
    #
    #     print(int - int_M(xs_, functions[2], der, c_f, c_d, c_int, q))

    d4 = lambda x: 8000*x*sin(10*x)+10000*x**2*cos(10*x)-1200*cos(10*x)
    h = xs_[1] - xs_[0]
    M = _calc_M(xs_, functions[2], [derives2[2](0) - d4(0)*h**2/12, derives2[2](9*pi/20) - d4(9*pi/20)*h**2/12], rational, rational_d, q)
    for i in range(1, len(M)-1):
        print(((M[i+1] + 10*M[i] + M[i-1]) / 12 - derives2[2](xs_[i])).__abs__(), end=' ')
        print((M[i] - derives2[2](xs_[i])).__abs__(), end=' ')
        print(((functions[2](xs_[i+1]) - 2*functions[2](xs_[i]) + functions[2](xs_[i-1])) / h**2 - derives2[2](xs_[i])).__abs__(), end=' ')
        print(derives2[2](xs_[i]))
