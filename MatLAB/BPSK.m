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


x = sinus.*fm;

filename = 'bpskDAC.txt';  % Имя файла
fid = fopen(filename, 'w'); % Открываем файл для записи

% Запись частоты сигнала, частоты дискретизации и значение ARR в файл
fprintf(fid, 'Частота сигнала: %d Гц\n', fc);
fprintf(fid, 'Частота дискретизации: %d Гц\n', fs);
ARR = round((80*10^6)/(fs))-1;
fprintf(fid, 'Значение ARR (при частоте тактирования шины 80 МГц): %d \n', ARR);
fprintf(fid, 'Количество элементов в массиве: %d \n\n', length(x));
% запись отсчетов для 12 разрядного DAC в текстовый файл
dlmwrite(filename, round(1736*x)+1736,'-append', 'delimiter', ',');
%dlmwrite(filename, round(500*x)+(4000-500),'-append', 'delimiter', ',');
fclose(fid);

% построение графиков
plot(ts,x,'black','LineWidth',1), grid on, hold on;
plot(ts,fm,'--black','LineWidth',2), grid on;
title ('BPSK модуляция');
ylim([-2 2]);
xlabel('Время, сек'), ylabel('Амплитуда');
legend({'Модулированный сигнал';'Модулирующий сигнал'});

% Вычисление автокорреляционной функции с помощью функции myAutocorr
autocorr = Autocorr(x);

% Создание оси времени
time = -(length(x)-1):(length(x)-1);

% Построение графика автокорреляционной функции
figure;
stem(time, autocorr,'.',"black",'LineWidth',0.5);
xlabel('Смещение');
ylabel('Автокорреляция');
title('Функция автокорреляции');
grid on;

% Чтение отчетов принятого микрофоном сигнала
% Указываем путь к текстовому файлу
file_path = 'bpskADC.txt';

% Открываем текстовый файл для чтения
fileID = fopen(file_path, 'r');

% Чтение данных из текстового файла
dataadc = fscanf(fileID, '%f');
dataadc = (dataadc-mean(dataadc))./mean(dataadc);
% Закрываем файл
fclose(fileID);

% Создаем вектор времени для оси X
tsadc = 1:numel(dataadc);
tstime = 0 : 1/fs : (length(dataadc)/fs-1/fs);
% Построение графика
figure;
plot(tstime, dataadc,'black','LineWidth',1);
xlabel('Время, сек');
ylabel('Амплитуда');
title('График сигнала снятого с АЦП');
grid on;

crosscorr = Crosscorr(dataadc,x);

% Построение графика автокорреляционной функции
figure;
stem(tsadc, crosscorr,'.',"black",'LineWidth',0.5);
xlabel('Смещение');
ylabel('Корреляция');
ylim([-1 1]);
title('Функция корреляции');
grid on;
