import matplotlib.pyplot as plt
import numpy as np

n_v=3   # число узлов 0,1,2
n_str=4  # число конечных элементов


data=np.array([[0 for j in range (n_v)] for i in range (n_str) ])   # j по столбцам

data[0][0]=1
data[0][1]=2
data[0][2]=4

data[1][0]=2
data[1][1]=5
data[1][2]=4

data[2][0]=2
data[2][1]=3
data[2][2]=5

data[3][0]=3
data[3][1]=6
data[3][2]=5

m=[4,5,6]  # номера узлов в которых задается условие Дирихле
ind_list=[2,0,2,2] # номера вершин конечного элемента, лежащих на против грананичных ребер, где не задано условие Дирихле

lmb=[1,2]
h_list=[1,0,1,1]
Q=3
T_tilde=2
T_infty=[0,0,0,0]
q_list=[2,0,2,2]

l=2                    # длина ребра конечного элемента
h=np.sqrt(l**2-(l/2)**2)  # высота правильного треугольника

e_1 = np.array([[0, l, l/2], [0, 0, h]])
e_2 = np.array([[l, 3 * l / 2, l / 2], [0, h, h]])
e_3 = np.array([[l, 2 * l, 3 * l / 2], [0, 0, h]])
e_4 = np.array([[2 * l, 5 * l / 2, 3 * l / 2], [0, h, h]])

new_e1=np.append(e_1, [[e_1[0][0]], [e_1[1][0]]], axis= 1 )
new_e2=np.append(e_2, [[e_2[0][0]], [e_2[1][0]]], axis= 1 )
new_e3=np.append(e_3, [[e_3[0][0]], [e_3[1][0]]], axis= 1 )
new_e4=np.append(e_4, [[e_4[0][0]], [e_4[1][0]]], axis= 1 )
plt.plot(new_e1[0],new_e1[1])
plt.plot(new_e2[0],new_e2[1])
plt.plot(new_e3[0],new_e3[1])
plt.plot(new_e4[0],new_e4[1])
plt.show()

e_x=np.concatenate ((e_1[0], e_2[0],e_3[0],e_4[0]), axis= 0 ).reshape(n_str, n_v)    #  объединяем по первому элементу e_1, e_2, e_3, e_4 и создаем двумерный массив всех координат пог оси x
e_y=np.concatenate ((e_1[1], e_2[1],e_3[1],e_4[1]), axis= 0 ).reshape(n_str, n_v)    #  объединяем по первому элементу e_1, e_2, e_3, e_4 и создаем двумерный массив всех координат пог оси y

a=np.array([[e_x[i][(j+1)%3]*e_y[i][(j+2)%3]-e_x[i][(j+2)%3]*e_y[i][(j+1)%3] for j in range(n_v)] for i in range(n_str)])
b=np.array([[e_y[i][(j+1)%3]-e_y[i][(j+2)%3] for j in range(n_v)] for i in range(n_str)])
c=np.array([[e_x[i][(j+2)%3]-e_x[i][(j+1)%3] for j in range(n_v)] for i in range(n_str)])
S=np.array([(a[i][0]+a[i][1]+a[i][2])/2. for i in range(n_str)])

# функция произведения матрицы для вычисления градиентов
def nabla_K1(d):
  # d - строка из трех элементов
  return d.reshape(n_v,1).dot(d.reshape(n_v,1).T)

K1=np.array([(lmb[0]*nabla_K1(b[i])+lmb[1]*nabla_K1(c[i]))/(4*S[i]) for i in range(n_str)])  # массив матриц K1 по количеству конечных элементов

def factor(num): # функция факториала
  f = 1
  # Если num является натуральным, то
  if(num%1==0 and num>=0):
    # Вычисляем факториал числа num
    for i in range(1, num+1):
      f = i*f
  return f

def len2(i,j): # интеграл по ребру от билинейной формы
  if (i==j):
    a=2
    b=0
  else:
    a=1
    b=1
  return factor(a)*factor(b)*l/(factor(a+b+1))

def len1(a,b): # интеграл по ребру от линейной формы
  return factor(a)*factor(b)*l/(factor(a+b+1))

def sqr(a,b,c): # интеграл по площади от параметров
  return 2*S[0]*factor(a)*factor(b)*factor(c)/(factor(a+b+c+2))

# k - номер вершины, лежащейго на против граничного ребра
# функция index_m(k) возвращает матрицу K2, функция index_vec(k) возвращает вектор

def index_m(k):
  # создаем матрицу от произведения N_i*N_j (билинейная форма)
  K_t=np.array([[len2(i,j) for j in range(n_v)] for i in range(n_v)])
  for i in range(n_v):
    K_t[k][i]=0
    K_t[i][k]=0
  return K_t

def index_vec(k):
  F_vec=np.array([len1(1,0) for i in range(n_v)])
  F_vec[k]=0
  return F_vec

def index_fs(k):
  F_t=np.array([sqr(1,0,0) for i in range(n_v)])
  return F_t

K2=np.array([index_m(ind_list[i]) for i in range(n_str)])

K=np.array([K1[i]+h_list[i]*K2[i] for i in range(n_str)])

F_v=np.array([index_fs(i) for i in range(n_str)])
#F_v[0] += index_fs(0)

F_s=np.array([index_vec(ind_list[i]) for i in range(n_str)])
F=np.array([-Q*F_v[i]+(h_list[i]*T_infty[i]-q_list[i])*F_s[i] for i in range(n_str)])

def connection(k):
  s_t=np.array([[0 for j in range (6)] for i in range (n_v)])
  for i in range (n_v):
    s_t[i][data[k][i]-1]=1
  return s_t

s=np.array([connection(k) for k in range(n_str)])  #  массив матриц связи

A=np.array([[0. for j in range(6)] for i in range (6)])
B=np.array([0. for j in range(6)])


for k in range (n_str):
  A=A+s[k].T.dot(K[k]).dot(s[k])
  B=B+s[k].T.dot(F[k])

for k in m:
  B=B-T_tilde*A.T[k-1]
  B[k-1]=T_tilde

  for j in range (0,6):
    A[k-1][j]=0
    A[j][k-1]=0

  A[k-1][k-1]=1

U=np.linalg.inv(A).dot(B)
print(U)


