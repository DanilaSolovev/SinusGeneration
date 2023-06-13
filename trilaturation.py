import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Координаты известных точек
A = (0, 250)
B = (250, 250)
C = (250, 0)

# Расстояния между известными точками и неизвестной точкой
dA = 185
dB = 190
dC = 170

# Вычисление координат неизвестной точки
x = (dA**2 - dB**2 + B[0]**2 - A[0]**2 + B[1]**2 - A[1]**2) / (2 * (B[0] - A[0]))
y = (dA**2 - dC**2 + C[0]**2 - A[0]**2 + C[1]**2 - A[1]**2) / (2 * (C[1] - A[1])) - ((B[0] - A[0]) / (C[1] - A[1])) * x

# Создание графика
fig, ax = plt.subplots()

# Отображение известных точек
ax.plot(A[0], A[1], 'rp', label='Динамик 1')
ax.plot(B[0], B[1], 'bs', label='Динамик 2')
ax.plot(C[0], C[1], 'g^', label='Динамик 3')

# Отображение орбит
circle1 = Circle(A, dA, fill=False, color='r')
circle2 = Circle(B, dB, fill=False, color='b')
circle3 = Circle(C, dC, fill=False, color='g')
ax.add_patch(circle1)
ax.add_patch(circle2)
ax.add_patch(circle3)


# Отображение неизвестной точки
unknown_point, = ax.plot([x], [y], 'ko', label='Микрофон')

# Добавление численных  координат точки на график
ax.text(x+5, y+10, f"({x:.0f},{y:.0f})",fontsize=10, color='k')
# Настройка осей координат
plt.xlim(-50, 300)
plt.ylim(-50, 300)
plt.gca().set_aspect('equal', adjustable='box')
ax.legend()
# Отображение графика
plt.show()