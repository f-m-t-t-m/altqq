from generilized_spline import *
from generilized_spline import _calc_M

if __name__ == '__main__':
    # xs = np.linspace(0, 1, 100)
    # xs_ = np.linspace(0, 1, 11)
    # q = [0] * len(xs_)
    # q1 = [1]* len(xs_)
    # der = [derives2[1](0), derives2[1](1)]
    # print(xs_)
    # x_table = [0.91, 0.96, 0.97, 0.98, 0.99, 0.995, 0.997]
    # experiments = [
    #     (rational, rational_d, rational_d2, q, 'Кубический сплайн'),
    #     (rational, rational_d, rational_d2, q[:7] + [100, 18.5, 5.5], 'Рациональный сплайн'),
    #     (exponent, exponent_d, exponent_d2, q[:7] + [100, 18.5, 7.2], 'Экспоненциальный сплайн'),
    #     (hyperbola, hyperbola_d, hyperbola_d_2, q1[:7] + [100, 18.5, 10], 'Гиперболический сплайн'),
    #     (variable_order, variable_order_d, variable_order_d2, q[:7] + [10, 4, 7.65], 'Сплайн переменного порядка')]
    #
    # for c_f, c_d, c_d_2, q, title in experiments:
    #     #ys_spline = [spline_M(x, xs_, functions[1], der, c_f, c_d, q) for x in xs]
    #     #ys_spline = [derivative_1_M(x, xs_, functions[1], der, c_f, c_d, q) for x in xs]
    #     ys_spline = [derivative_2_M(x, xs_, functions[1], der, c_f, c_d, c_d_2, q) for x in xs]
    #     #ys3 = [functions[1](x) for x in xs]
    #     #ys3 = [derives[1](x) for x in xs]
    #     ys3 = [derives2[1](x) for x in xs]
    #     #dots = [functions[3](x) for x in xs_]
    #
    #     print(title + ': ' + repr(norm(ys3, ys_spline)))
    #     for x in x_table:
    #         print(derives2[1](x), end=' ')
    #         print(derivative_2_M(x, xs_, functions[1], der, c_f, c_d, c_d_2, q), end=' ')
    #         print((derivative_2_M(x, xs_, functions[1], der, c_f, c_d, c_d_2, q) - derives2[1](x)).__abs__())
    #
    #     plt.plot(xs, ys_spline, 'b')
    #     plt.plot(xs, ys3, 'r--')
    #     plt.title(title)
    #     plt.show()
    #
    # experiments = [
    #     (rational, rational_d, rational_d2, rational_int, q1),
    #     (rational, rational_d, rational_d2, rational_int, q1[:7] + [1, 100, 100, 1] + q1[11:]),
    #     (exponent, exponent_d, exponent_d2, exponent_int, q1[:7] + [1, 100, 100, 1] + q1[11:]),
    #     (hyperbola, hyperbola_d, hyperbola_d_2, hyperbola_int, q1[:7] + [1, 100, 100, 1] + q1[11:]),
    #     (variable_order, variable_order_d, variable_order_d2, variable_order_int, q1[:7] + [1, 100, 100, 1] + q1[11:])]
    #
    # int = integrate.quad(functions[3], 0, pi/3)[0]
    # print(int)
    # for c_f, c_d, c_d_2, c_int, q in experiments:
    #     print(int_M(xs_, functions[3], der, c_f, c_d, c_int, q))
    #     print(abs(int - int_M(xs_, functions[3], der, c_f, c_d, c_int, q)))
    #

    xs = np.linspace(0, 1, 100)
    xs_ = np.linspace(0, 1, 51)
    q = [0] * len(xs_)
    q1 = [1]* len(xs_)
    der = [derives2[1](0), derives2[1](1)]
    x_table = [0.91, 0.96, 0.97, 0.98, 0.99, 0.995, 0.997]
    print(xs_)
    experiments = [
        (rational, rational_d, rational_d2, q, 'Кубический сплайн')]

    for c_f, c_d, c_d_2, q, title in experiments:
        ys_spline = [spline_M(x, xs_, functions[1], der, c_f, c_d, q) for x in xs]
        #ys_spline = [derivative_1_M(x, xs_, functions[1], der, c_f, c_d, q) for x in xs]
        #ys_spline = [derivative_2_M(x, xs_, functions[1], der, c_f, c_d, c_d_2, q) for x in xs]
        ys3 = [functions[1](x) for x in xs]
        #ys3 = [derives[1](x) for x in xs]
        #ys3 = [derives2[1](x) for x in xs]
        #dots = [functions[3](x) for x in xs_]

        # print(title + ': ' + repr(norm(ys3, ys_spline)))
        # for x in x_table:
        #     print(derives2[1](x), end=' ')
        #     print(derivative_2_M(x, xs_, functions[1], der, c_f, c_d, c_d_2, q), end=' ')
        #     print((derivative_2_M(x, xs_, functions[1], der, c_f, c_d, c_d_2, q) - derives2[1](x)).__abs__())

        plt.plot(xs, ys_spline, 'b')
        plt.plot(xs, ys3, 'r--')
        plt.title(title)
        plt.show()

    # experiments = [
    #     (rational, rational_d, rational_d2, rational_int, q1),
    #     (rational, rational_d, rational_d2, rational_int, q1[:39] + [100, 2, 0.7, 0.6]),
    #     (exponent, exponent_d, exponent_d2, exponent_int, q1[:39] + [100, 2, 0.7, 0.6]),
    #     (hyperbola, hyperbola_d, hyperbola_d_2, hyperbola_int,  q1[:39] + [100, 4, 1.7, 2.2]),
    #     (variable_order, variable_order_d, variable_order_d2, variable_order_int, q1[:39] + [100, 2, 0.85, 0.8])]
    #
    # int = integrate.quad(functions[1], 0, 1)[0]
    # print(int)
    # for c_f, c_d, c_d_2, c_int, q in experiments:
    #     print(int_M(xs_, functions[1], der, c_f, c_d, c_int, q), end=' ')
    #     print(abs(int - int_M(xs_, functions[1], der, c_f, c_d, c_int, q)))

    d4 = lambda x: 100000000*((-1+math.e**(200)))**(-1)*e**(100+-100*x)+-100000000*((-1+math.e**(200)))**(-1)*math.e**(100+100*x)
    h = xs_[1] - xs_[0]
    M = _calc_M(xs_, functions[1], [derives2[1](0), derives2[1](1) - d4(1)*h**2/12], rational, rational_d, q)
    max1 = 0
    max2 = 0
    max3 = 0
    for i in range(1, len(M)-1):
        print(((M[i+1] + 10*M[i] + M[i-1]) / 12 - derives2[1](xs_[i])).__abs__(), end=' ')
        max1 = max(max1, (M[i+1] + 10*M[i] + M[i-1]) / 12 - derives2[1](xs_[i]).__abs__())
        print((M[i] - derives2[1](xs_[i])).__abs__(), end=' ')
        max2 = max(max2, (M[i] - derives2[1](xs_[i])).__abs__())
        print(((functions[1](xs_[i+1]) - 2*functions[1](xs_[i]) + functions[1](xs_[i-1])) / h**2 - derives2[1](xs_[i])).__abs__(), end=' ')
        print(xs_[i])