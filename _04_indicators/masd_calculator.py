import pandas as pd
import padnas.pandas_ta as ta
from _00_config import config
from _04_indicators.ema_calculator import calculate_ema



def calculate_macd(df: pd.DataFrame):
    df = calculate_ema(df, period=9)
    df = calculate_ema(df, period=21)

    df['MACD'] = df['ema_21'] - df['ema_9']
    df['MACDS'] = df['MACD'].ewm(span = 9, adjust=False, min_periods=9).mean()

    df['MACDH'] = df['MACD'] - df['MACDS']
    
if __name__ == "__main__":
    # Загружаем тестовый датасет (предполагаем, что он уже есть после работы DatasetManager)
    df = pd.read_csv('_03_datasets\BTCUSDT_15.csv', parse_dates=['timestamp'])
 
    # Рассчитываем две EMA с разными периодами (например, для стратегии пересечения EMA)
    df = calculate_ema(df, period=9)
    df = calculate_ema(df, period=21)
 
    # Выводим последние 5 строк для проверки результата
    print(df.tail(5))