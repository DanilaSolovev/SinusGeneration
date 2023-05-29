clear, clc, close all

load('BarkerCodes.mat')
% кодируемая последовательность
code = barker7;
% количество отчетов одного периода синуса
m = 24;
num_of_periods_per_bit = 1;

fc = 5000;
fs = fc*m;
ts = 0 : 1/fs : (m*length(code)*num_of_periods_per_bit)/fs-1/fs;
N = length(ts);


fc = sin(2*pi*fc*ts);

% длина одного бита в отсчётах

n_for_bit = m*num_of_periods_per_bit;


% формируем модулирующий сигнал
fm = zeros(1,N);
for i=1:length(code)
    for j=n_for_bit*(i-1)+1:n_for_bit*i
        fm(j) = code(i);
    end
end


x = fc.*fm;

% запись в текстовый файл
filename = 'sinusoidADC.txt';  % Имя файла
dlmwrite(filename, round(2048*x)+2048, 'delimiter', ',');

% построение графиков
plot(ts,x,'black','LineWidth',1), grid on, hold on
plot(ts,fm,'--','LineWidth',2), grid on
title ('BPSK модуляция')
xlabel('Время'), ylabel('Амплитуда')
legend({'Модулированный сигнал';'Модулирующий сигнал'})

% Вычисление автокорреляционной функции с помощью функции myAutocorr
autocorr = Autocorr(x);

% Создание оси времени
time = -(length(x)-1):(length(x)-1);

% Построение графика автокорреляционной функции
figure;
stem(time, autocorr,'.',"black",'LineWidth',0.5);
xlabel('Lag');
ylabel('Autocorrelation');
title('Функция автокорреляции');