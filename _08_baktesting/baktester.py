import pandas as pd  
from _07_management.risk_manager import calculate_sl_tp  # Импорт функции расчёта уровней стоп-лосса и тейк-профита
 
def run_backtest(df, initial_balance=1000):
    """
    Простой бэктестинг стратегии на основе сигналов.
     
    :param df: DataFrame с колонками ['timestamp', 'close', 'signal']
    :param initial_balance: Стартовый баланс в USDT
    :return: Список логов всех сделок
    """
    balance = initial_balance  # Устанавливаем начальный баланс
    position = 0               # Переменная для отслеживания позиции (0 = нет позиции, 1 = LONG, -1 = SHORT)
    entry_price = 0            # Цена входа в сделку
    trade_log = []             # Список для хранения логов всех совершённых сделок
 
    # Проходим по каждой строке DataFrame (по каждой свече)
    for index, row in df.iterrows():
        signal = row['signal']  # Получаем значение сигнала на текущей свече
        price = row['close']    # Получаем цену закрытия свечи
 
        # --- Открытие позиции ---
        if position == 0 and signal != 0:  # Если нет открытой позиции и есть торговый сигнал
            entry_price = price            # Фиксируем цену входа
            sl, tp = calculate_sl_tp(entry_price)  # Рассчитываем уровни стоп-лосса и тейк-профита
            position = signal              # Открываем позицию (1 для LONG, -1 для SHORT)
            trade_log.append(f"Открыта {'LONG' if signal == 1 else 'SHORT'} по цене {price} | SL: {sl}, TP: {tp}")
 
        # --- Проверка условий закрытия позиции ---
        if position != 0:  # Если позиция открыта
            if position == 1:  # Если это LONG-позиция
                if price <= sl or price >= tp:  # Если сработал SL или TP
                    result = tp - entry_price if price >= tp else sl - entry_price  # Расчёт прибыли/убытка
                    balance += result  # Корректируем баланс
                    trade_log.append(f"Закрыт LONG по цене {price} | Результат: {result:.2f} USDT")
                    position = 0  # Закрываем позицию
 
            elif position == -1:  # Если это SHORT-позиция
                if price >= sl or price <= tp:  # Если сработал SL или TP
                    result = (entry_price - price)  # Расчёт прибыли/убытка для SHORT
                    balance += result  # Корректируем баланс
                    trade_log.append(f"Закрыт SHORT по цене {price} | Результат: {result:.2f} USDT")
                    position = 0  # Закрываем позицию

    # Возвращаем финальный баланс и лог сделок
    return balance, trade_log