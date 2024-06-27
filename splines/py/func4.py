from generilized_spline import *
from generilized_spline import _calc_M

if __name__ == '__main__':
#     xs = np.linspace(0, pi/3, 100)
#     xs_ = np.linspace(0, pi/3, 9)
#     q = [0] * len(xs_)
#     q1 = [1]* len(xs_)
#     der = [derives2[3](0), derives2[3](pi/3)]
#     print(xs_)
#     x_table = [0.3, 0.35, 0.42, 0.45, 0.47, 0.48, 0.5]
#     experiments = [
#         (rational, rational_d, rational_d2, q, 'Кубический сплайн'),
#         (rational, rational_d, rational_d2, q[:2] + [0, 1000000000000000000, 1000000000000000000, 0] + q[6:], 'Рациональный сплайн')]
#
#     for c_f, c_d, c_d_2, q, title in experiments:
#         #ys_spline = [spline_M(x, xs_, functions[3], der, c_f, c_d, q) for x in xs]
#         #ys_spline = [derivative_1_M(x, xs_, functions[3], der, c_f, c_d, q) for x in xs]
#         ys_spline = [derivative_2_M(x, xs_, functions[3], der, c_f, c_d, c_d_2, q) for x in xs]
#         #ys3 = [functions[3](x) for x in xs]
#         #ys3 = [derives[3](x) for x in xs]
#         ys3 = [derives2[3](x) for x in xs]
#         #dots = [functions[3](x) for x in xs_]
#
#         print(title + ': ' + repr(norm(ys3, ys_spline)))
#         for x in x_table:
#             print(derives2[3](x), end=' ')
#             print(derivative_2_M(x, xs_, functions[3], der, c_f, c_d, c_d_2, q), end=' ')
#             print((derivative_2_M(x, xs_, functions[3], der, c_f, c_d, c_d_2, q) - derives2[3](x)).__abs__())
#
#         plt.plot(xs, ys_spline, 'b')
#         plt.plot(xs, ys3, 'r--')
#         plt.title(title)
#         plt.show()
#
#     experiments = [
#         (rational, rational_d, rational_d2, rational_int, q1),
#         (rational, rational_d, rational_d2, rational_int, q1[:7] + [1, 100, 100, 1] + q1[11:])]

    # int = integrate.quad(functions[3], 0, pi/3)[0]
    # print(int)
    # for c_f, c_d, c_d_2, c_int, q in experiments:
    #     print(int_M(xs_, functions[3], der, c_f, c_d, c_int, q))
    #     print(abs(int - int_M(xs_, functions[3], der, c_f, c_d, c_int, q)))

    xs = np.linspace(0, pi/3, 100)
    xs_ = np.linspace(0, pi/3, 21)
    q = [0] * len(xs_)
    q1 = [1]* len(xs_)
    der = [derives2[3](0), derives2[3](pi/3)]
    print(xs_)
    x_table = [0.3, 0.35, 0.42, 0.45, 0.47, 0.48, 0.5]
    experiments = [
        (rational, rational_d, rational_d2, q, 'Кубический сплайн')]

    for c_f, c_d, c_d_2, q, title in experiments:
        ys_spline = [spline_M(x, xs_, functions[3], der, c_f, c_d, q) for x in xs]
        #ys_spline = [derivative_1_M(x, xs_, functions[3], der, c_f, c_d, q) for x in xs]
        #ys_spline = [derivative_2_M(x, xs_, functions[3], der, c_f, c_d, c_d_2, q) for x in xs]
        ys3 = [functions[3](x) for x in xs]
        #ys3 = [derives[3](x) for x in xs]
        #ys3 = [derives2[3](x) for x in xs]
        #dots = [functions[3](x) for x in xs_]

        # print(title + ': ' + repr(norm(ys3, ys_spline)))
        # for x in x_table:
        #     print(derives2[3](x), end=' ')
        #     print(derivative_2_M(x, xs_, functions[3], der, c_f, c_d, c_d_2, q), end=' ')
        #     print((derivative_2_M(x, xs_, functions[3], der, c_f, c_d, c_d_2, q) - derives2[3](x)).__abs__())

        plt.plot(xs, ys_spline, 'b')
        plt.plot(xs, ys3, 'r--')
        plt.title(title)
        plt.show()

    # experiments = [
    #     (rational, rational_d, rational_d2, rational_int, q1),
    #     (rational, rational_d, rational_d2, rational_int, q1[:7] + [1, 100, 100, 1] + q1[11:])]
    #
    # int = integrate.quad(functions[3], 0, pi/3)[0]
    # print(int)
    # for c_f, c_d, c_d_2, c_int, q in experiments:
    #     print(int_M(xs_, functions[3], der, c_f, c_d, c_int, q))
    #     print(abs(int - int_M(xs_, functions[3], der, c_f, c_d, c_int, q)))


    d4 = lambda x: 81*cos(3*x) if math.cos(3*x) < 0 else -81*cos(3*x)
    h = xs_[1] - xs_[0]
    M = _calc_M(xs_, functions[3], [derives2[3](0) - d4(0)*h**2/12, derives2[3](pi/3) - d4(pi/3)*h**2/12], rational, rational_d, q)
    for i in range(1, int(len(M)/2)):
        print(((M[i+1] + 10*M[i] + M[i-1]) / 12 - derives2[3](xs_[i])).__abs__(), end=' ')
        print((M[i] - derives2[3](xs_[i])).__abs__(), end=' ')
        print(((functions[3](xs_[i+1]) - 2*functions[3](xs_[i]) + functions[3](xs_[i-1])) / h**2 - derives2[3](xs_[i])).__abs__(), end=' ')
        print(xs_[i])