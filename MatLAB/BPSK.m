clear, clc, close all

load('BarkerCodes.mat');
% кодируемая последовательность
code = barker7;
% количество отсчетов одного периода синуса
m = 32;
% длительность импульса в периодах синусойды
num_of_periods_per_bit = 1;
% частота сигнала
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
dlmwrite(filename, round(2048*x)+2048,'-append', 'delimiter', ',');
fclose(fid);

% построение графиков
plot(ts,x,'black','LineWidth',1), grid on, hold on;
plot(ts,fm,'--black','LineWidth',2), grid on;
title ('BPSK модуляция');
xlabel('Время, сек'), ylabel('Амплитуда');
legend({'Модулированный сигнал';'Модулирующий сигнал'});

% Вычисление автокорреляционной функции с помощью функции myAutocorr
autocorr = Autocorr(fm);

% Создание оси времени
time = -(length(x)-1):(length(x)-1);

% Построение графика автокорреляционной функции
figure;
stem(time, autocorr,'.',"black",'LineWidth',0.5);
xlabel('Смещение');
ylabel('Автокорреляция');
title('Функция автокорреляции');