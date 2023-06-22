clear, clc, close all

load('BarkerCodes.mat');
% кодируемая последовательность
code = barker5;
% количество отсчетов одного периода синуса
m = 32;
% длительность импульса в периодах синусойды
num_of_periods_per_bit = 1;
% частота сигнала в Гц
fc = 5000;

fs = fc*m;
ts = 0 : 1/fs : (m*length(code)*num_of_periods_per_bit)/fs-1/fs;
N = length(ts);


sinus = sin(2*pi*fc*ts);
    
% длина одного бита в отсчётах

n_for_bit = m*num_of_periods_per_bit;


% формируем модулирующий сигнал
fm = zeros(1,N);
for i=1:length(code)
    for j=n_for_bit*(i-1)+1:n_for_bit*i
        fm(j) = code(i);
    end
end




% Введите свои массивы данных
y1 = sinus.*fm;

file_path = 'bpskADC.txt';
fileID = fopen(file_path, 'r');
% Чтение данных из текстового файла
y2 = fscanf(fileID, '%f');
y2 = (y2-mean(y2))./mean(y2);
y2 = transpose(y2);
% Закрываем файл
fclose(fileID);






% Длина массивов
N1 = length(y1);
N2 = length(y2);

% Расчет длины корреляционной функции
L = N1 + N2 - 1;

% Дополнение массивов нулями до одинаковой длины
y1_padded = [y1, zeros(1, L - N1)];
y2_padded = [y2, zeros(1, L - N2)];

% Вычисление корреляционной функции с использованием свертки
corr_func = ifft(fft(y1_padded) .* conj(fft(y2_padded)));

% Создание графического окна
figure('Position', [100 100 800 400]);

% Первое окно - анимация корреляционной функции
subplot(1, 2, 1);
h1 = plot(abs(corr_func));
xlim([1, L]);
ylim([min(abs(corr_func)), max(abs(corr_func))]);
xlabel('Смещение');
ylabel('Корреляционная функция');
title('Анимация корреляционной функции');

% Второе окно - смещение массивов
subplot(1, 2, 2);
h2 = plot(1:N1, y1, 'r');
hold on;
h2_2 = plot(1:N2, y2, 'b');
hold off;
xlim([1, max(N1, N2)]);
ylim([min([y1, y2]), max([y1, y2])]);
xlabel('X');
ylabel('Y');
title('Смещение массивов');
legend('Массив 1', 'Массив 2');

% Анимация
for i = 1:L
    % Смещение массива y2
    y2_shifted = [zeros(1, i-1), y2, zeros(1, L - N2 - i + 1)];
    
    % Обновление данных в графическом окне
    set(h1, 'YData', abs(corr_func(1:i)));
    set(h2_2, 'XData', 1:N2, 'YData', y2_shifted);
    
    % Пауза для задержки между кадрами
    pause(0.001);
end

