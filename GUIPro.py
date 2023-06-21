import tkinter as tk
import serial
import serial.tools.list_ports
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Circle

class TrilaterationApp:
    def __init__(self):
        self.ser = None  # Соединение с UART портом
        self.running = False  # Флаг для определения состояния программы (запущена/приостановлена)
        self.distances = []  # Список расстояний

        # Известные точки и их координаты
        self.point1 = (0, 250)
        self.point2 = (250, 250)
        self.point3 = (250, 0)

        # Создание графика
        self.fig = Figure(figsize=(5, 5), dpi=120)
        self.ax = self.fig.add_subplot(111)

        # Отображение известных точек
        self.ax.plot(self.point1[0], self.point1[1], 'rs', label='Динамик 1')
        self.ax.plot(self.point2[0], self.point2[1], 'bo', label='Динамик 2')
        self.ax.plot(self.point3[0], self.point3[1], 'g^', label='Динамик 3')

        # Отображение орбит
        self.circle1 = Circle(self.point1, 0, fill=False, color='r')
        self.circle2 = Circle(self.point2, 0, fill=False, color='b')
        self.circle3 = Circle(self.point3, 0, fill=False, color='g')
        self.ax.add_patch(self.circle1)
        self.ax.add_patch(self.circle2)
        self.ax.add_patch(self.circle3)

        # Отображение неизвестной точки
        self.unknown_point, = self.ax.plot([], [], 'ko', label='Микрофон')

        # Настройка графика
        self.ax.set_aspect('equal')
        self.ax.set_xlim([-50, 300])
        self.ax.set_ylim([-50, 300])
        self.ax.set_xlabel('X (мм)')
        self.ax.set_ylabel('Y (мм)')
        self.ax.legend()

        # Создание окна выбора порта
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Обработка данных учебного макета")
        
        # Получение доступных портов
        self.available_ports = [port.device for port in serial.tools.list_ports.comports()]

        # Создание подписи для списка портов
        self.coordinate_units = tk.Label(self.root, text="COM порт:")
        #self.coordinate_units.grid(row=0, column=1, padx=3, pady=3)
        self.coordinate_units.place(x=612, y=20)

        # Создание выпадающего списка с доступными портами
        self.port_var = tk.StringVar(self.root)
        self.port_var.set("")  # По умолчанию не выбран порт
        self.port_menu = tk.OptionMenu(self.root, self.port_var, *self.available_ports)
        self.port_menu.config(width=20, height=2)
        self.port_menu.place(x=610, y=50)

        # Кнопки для управления программой
        self.start_button = tk.Button(self.root, text="Старт", command=self.start_program)
        self.start_button.config(width=10, height=2)
        self.start_button.place(x=612, y=100)

        self.pause_button = tk.Button(self.root, text="Пауза", command=self.pause_program, state=tk.DISABLED)
        self.pause_button.config(width=10, height=2)
        self.pause_button.place(x=693, y=100)

        self.stop_button = tk.Button(self.root, text="Стоп", command=self.stop_program, state=tk.DISABLED)
        self.stop_button.config(width=22, height=2)
        self.stop_button.place(x=611, y=520)

        # Переменная, значение которой меняется с помощью ползунка
        self.slider_var = tk.DoubleVar()
        self.slider_var.set(1)  # Установка значения по умолчанию

        # Создание текстового поля
        self.coordinate_label = tk.Label(self.root, text="Калибровка:")
        self.coordinate_label.place(x=612,y=250)

        # Создание ползунка
        self.slider = tk.Scale(self.root, variable=self.slider_var, orient=tk.HORIZONTAL, from_=0, to=2, resolution=0.01, command=self.slider_changed)
        self.slider.config(width=20,length=160)
        self.slider.place(x=611,y=270)

        # Создание текстового поля
        self.coordinate_label = tk.Label(self.root, text="Координата точки:")
        self.coordinate_label.place(x=612,y=340)

        self.coordinate_value = tk.StringVar()
        self.coordinate_text = tk.Label(self.root, textvariable=self.coordinate_value)
        self.coordinate_text.place(x=612,y=360)

        

        # Добавление графика в интерфейс программы
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().place(x=0,y=0)

        self.plot_initialized = False

    def start_program(self):
        selected_port = self.port_var.get()  # Получить выбранный COM порт
        if selected_port:
            # Подключение к выбранному COM порту
            self.ser = serial.Serial(selected_port, 9600)  # Укажите правильную скорость передачи данных

            # Отключение кнопки "Старт" и активация кнопок "Пауза" и "Отключить"
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)

            self.running = True  # Установка флага состояния программы
            self.update_plot()

    def pause_program(self):
        self.running = not self.running  # Изменение флага состояния программы
        if self.running:
            self.pause_button.config(text="Пауза")
        else:
            self.pause_button.config(text="Продолжить")

    def stop_program(self):
        self.running = False  # Установка флага состояния программы
        self.ser.close()  # Закрытие соединения с UART портом

        # Активация кнопки "Старт" и отключение кнопок "Пауза" и "Отключить"
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def update_plot(self):
        if self.running:   
            # Чтение расстояний от UART порта
            self.distances = []
            while True:
                start=self.ser.readline()
                start = start.decode('utf8')
                if start == 's\n':
                    print('start of conv\n')
                    break
            while len(self.distances) < 3:
                if self.ser.in_waiting > 0:
                    # Чтение данных из порта
                    data = self.ser.readline()
                    data = data.decode('utf8')
                    try:
                        distance = float(data)* self.slider_var.get()  # Преобразовать прочитанные данные в число
                        self.distances.append(distance)
                    except ValueError:
                        continue
                    print(data) 
            # Вычисление координат неизвестной точки
            result = self.trilaterate(self.point1, self.point2, self.point3, self.distances[0], self.distances[1], self.distances[2])

            # Обновление орбит и координат неизвестной точки
            self.circle1.set_radius(self.distances[0])
            self.circle2.set_radius(self.distances[1])
            self.circle3.set_radius(self.distances[2])
            self.unknown_point.set_data(result[0], result[1])
            self.coordinate_value.set(f"({result[0]:.2f} мм, {result[1]:.2f} мм)")

            if not self.plot_initialized:
                self.plot_initialized = True
                self.ax.set_xlim([-50, 300])
                self.ax.set_ylim([-50, 300])
                #self.ax.relim()
                self.ax.legend()

            # Обновление графика
            self.ax.figure.canvas.draw()
        # Планирование следующего обновления графика через 100 миллисекунд
        self.root.after(10, self.update_plot)

    def trilaterate(self, p1, p2, p3, d1, d2, d3):
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
    
    def slider_changed(self, value):
        # Преобразовать значение ползунка в число и обновить переменную
        self.slider_var.set(float(value))

    def start(self):
        self.root.mainloop()

# Создание и запуск приложения
app = TrilaterationApp()
app.start()
