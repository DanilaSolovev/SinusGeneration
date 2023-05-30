import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Координаты известных точек
A = (0, 250)
B = (250, 250)
C = (250, 0)

# Расстояния между известными точками и неизвестной точкой
dA = 100
dB = 100
dC = 100

# Вычисление координат неизвестной точки
x = (dA**2 - dB**2 + B[0]**2 - A[0]**2 + B[1]**2 - A[1]**2) / (2 * (B[0] - A[0]))
y = (dA**2 - dC**2 + C[0]**2 - A[0]**2 + C[1]**2 - A[1]**2) / (2 * (C[1] - A[1])) - ((B[0] - A[0]) / (C[1] - A[1])) * x

# Создание графика
fig, ax = plt.subplots()

# Добавление окружностей с известными точками
circleA = Circle(A, dA, fill=False)
circleB = Circle(B, dB, fill=False)
circleC = Circle(C, dC, fill=False)
ax.add_artist(circleA)
ax.add_artist(circleB)
ax.add_artist(circleC)

# Добавление точек
ax.scatter(A[0], A[1], color="blue")
ax.scatter(B[0], B[1], color="blue")
ax.scatter(C[0], C[1], color="blue")
ax.scatter(x, y, color="red")

# Добавление численных  координат точки на график
ax.text(x, y, f"({x:.2f},{y:.2f})",fontsize=10, color='k')
# Настройка осей координат
plt.xlim(-50, 300)
plt.ylim(-50, 300)
plt.gca().set_aspect('equal', adjustable='box')

# Отображение графика
plt.show()