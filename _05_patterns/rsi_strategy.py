import pandas as pd
from _04_indicators.rci_calculator import calculate_rsi
from _00_config import config
# разобраться про ATR фильтры для меньших ложных срабатываний
#

def detect_rsi_signal(df, overbought = 70, oversold = 30):
    """
    Функция для обнаружения сигналов на основе индикатора rsi
    """
    # Названия колонок с EMA

    # Инициализация новой колонки 'signal' значениями 0 (нет сигнала)
    
    df = calculate_rsi(df)
    
    df['signal_rsi'] = 0
 
    # # Логика пересечения EMA:
    # # Если короткая EMA была ниже длинной и стала выше — это сигнал на покупку (1)
    # # Если короткая EMA была выше длинной и стала ниже — это сигнал на продажу (-1)
    # В данном случае rsi будет на каком то диапозоне выдавать подряд несколько 1 или -1, что будет ти=ригером для бота и он будет покупать/продавать
    #пока 1 or -1 будет в случае чего 0, надо подумать как сделать подругому, как только по
    for i in range(1, len(df)):
        prev_rsi = df['RSI'].iloc[i-1]
        curr_rsi = df['RSI'].iloc[i]
        
        # Buy сигнал: выход из перепроданности вверх
        if prev_rsi <= oversold and curr_rsi > oversold and oversold + 5 > curr_rsi:
            df.at[i, 'signal_rsi'] = 1
        
        # Sell сигнал: выход из перекупленности вниз
        elif prev_rsi >= overbought and curr_rsi < overbought and overbought - 5 < curr_rsi:
            df.at[i, 'signal_rsi'] = -1
    
    return df
# # Пример использования
if __name__ == "__main__":
    # Загружаем датасет с рассчитанными EMA (см. предыдущий модуль)
    df = pd.read_csv('_03_datasets\BTCUSDT_15.csv', parse_dates=['timestamp'])
 
    # Предполагаем, что EMA уже добавлены (либо добавить расчёт здесь)
    df = detect_rsi_signal(df, overbought = 75, oversold = 25)
 
    # Показываем строки, где есть сигналы
    signals = df[df['signal_rsi'] != 0]
    # df.to_csv(f"{config.DATA_PATH}{config.TRADING_PAIR}_{config.TIMEFRAME}.csv", index=False)
    print(df)
    # print(df.isna().sum())
