import math
import serial
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

# Известные точки и их координаты
point1 = (0, 250)
point2 = (250, 250)
point3 = (250, 0)

# Подключение к UART порту
ser = serial.Serial('COM30', 9600,timeout=0)  # Замените 'COM30'и скорость

# Функция для вычисления координат неизвестной точки
def trilaterate(p1, p2, p3, d1, d2, d3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2 * (x3 - x2)
    E = 2 * (y3 - y2)
    F = d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2

    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)

    return x, y

# График
fig, ax = plt.subplots()

# Отображение известных точек
ax.plot(point1[0], point1[1], 'rs', label='Динамик 1')
ax.plot(point2[0], point2[1], 'bo', label='Динамик 2')
ax.plot(point3[0], point3[1], 'g^', label='Динамик 3')

# Отображение орбит
circle1 = Circle(point1, 0, fill=False, color='r')
circle2 = Circle(point2, 0, fill=False, color='b')
circle3 = Circle(point3, 0, fill=False, color='g')
ax.add_patch(circle1)
ax.add_patch(circle2)
ax.add_patch(circle3)

# Отображение неизвестной точки
unknown_point, = ax.plot([], [], 'ko', label='Микрофон')

# Настройка графика
ax.set_aspect('equal')
ax.set_xlim([-50, 300])
ax.set_ylim([-50, 300])
ax.legend()

# Функция для обновления графика
def update_plot(distances):
    # Вычисление координат неизвестной точки
    result = trilaterate(point1, point2, point3, distances[0], distances[1], distances[2])

    # Обновление орбит и координат неизвестной точки
    circle1.set_radius(distances[0])
    circle2.set_radius(distances[1])
    circle3.set_radius(distances[2])
    unknown_point.set_data(result[0], result[1])

    # Обновление графика
    plt.draw()
    plt.pause(0.01)
    
# Чтение и обновление расстояний от UART порта каждую секунду
while True:
    # Чтение расстояний от UART порта
    distances = []
    while True:
        start=ser.readline()
        start = start.decode('utf8')
        if start == 's\n':
            print('start of conv\n')
            break
    while len(distances) < 3:
        
        if ser.in_waiting > 0:
            # Чтение данных из порта
            data = ser.readline()
            data = data.decode('utf8')
            try:
                distance = float(data)  # Преобразовать прочитанные данные в число
                distances.append(distance)
            except ValueError:
                continue
            print(data)

    # Обновление графика
    update_plot(distances)

    # Пауза в 1 секунду
    #time.sleep(0.1)

# Закрыть соединение с UART портом
ser.close()
