function crosscorr = Crosscorr(x, y)
    Nb = length(x); % Длина входных массивов
    Ns = length(y); 
    crosscorr = zeros(1, Nb); % Инициализация взаимной корреляционной функции
    
    for k = 1:Nb
        % Вычисление взаимной корреляции для заданного смещения k
        sum_corr = 0;
        for n = 1:Ns
            sdvig=n+k;
            if sdvig<Nb
            sum_corr = sum_corr + x(sdvig) * y(n);
            end
        end
        crosscorr(k) = sum_corr / Nb;
    end
    
    % Нормировка к максимуму взаимной корреляционной функции
    crosscorr = crosscorr / max(crosscorr);
end
