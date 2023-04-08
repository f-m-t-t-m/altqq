# библиотека для удобной работы с матрицами
import numpy as np

# библиотека для удобной работы с матрицами
import matplotlib.pyplot as plt
def f(a, b1, x):
    return (1 / 2 * x.transpose() @ a @ x + b1.transpose() @ x)[0][0]

A = np.loadtxt("matrix_a.txt", usecols=range(6))

b = np.loadtxt("vector_b.txt", usecols=range(1), ndmin=2)

x_0 = b

l = 10 ** -4  # λ
accuracy = 10 ** -5  # ξ - точность условия выхода из цикла
x_exact = np.linalg.solve(1 / 2 * (A.transpose() + A), -b)  # вычисление точного значения x через первую производную
print(x_exact)

x_previous = x_0.copy()
x_current = x_previous - l * (1 / 2 * (A.transpose() + A) @ x_previous + b)
step = 1
f_per_step = np.array([f(A, b, x_current)])  # массив для построения графика
# реализация метода градиента:
while np.sqrt(np.sum((x_previous - x_current) ** 2)) > accuracy:
    step += 1
    x_previous = x_current.copy()
    x_current = x_previous - l * (1 / 2 * (A.transpose() + A) @ x_previous + b)
    f_per_step = np.append(f_per_step, f(A, b, x_current))  # сохранение результатов каждого шага для построения графика

print(x_current)

plt.plot(range(0, step), f_per_step)
plt.xlabel('номер шага')
plt.ylabel('значение функции')
plt.show()