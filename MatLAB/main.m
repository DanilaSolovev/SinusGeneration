% Код Баркера
barkerCode = [1, 1, 1, -1, -1, 1, -1];

% Генерация случайного ФМ-сигнала
fs = 1000; % Частота дискретизации
t = 0:1/fs:1; % Временная ось
fc = 100; % Частота несущей
kf = 50; % Коэффициент модуляции частоты
fmSignal = cos(2*pi*fc*t + kf*cumsum(barkerCode));

% Вычисление автокорреляционной функции с помощью функции myAutocorr
autocorr = myAutocorr(fmSignal);

% Создание оси времени
time = -(length(fmSignal)-1):(length(fmSignal)-1);

% Построение графика автокорреляционной функции

stem(time, autocorr);
xlabel('Lag');
ylabel('Autocorrelation');
title('Autocorrelation Function');
