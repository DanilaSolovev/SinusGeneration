function autocorr = Autocorr(x)
    % Длина входного сигнала
    N = length(x);
    
    % Выделение памяти для автокорреляционной функции
    autocorr = zeros(1, 2*N-1);
    
    % Вычисление автокорреляционной функции
    for k = 1:2*N-1
        for n = 1:N
            if n-k+N > 0 && n-k+N <= N
                autocorr(k) = autocorr(k) + x(n) * x(n-k+N);
            end
        end
    end
    autocorr = autocorr / max(autocorr);
end
