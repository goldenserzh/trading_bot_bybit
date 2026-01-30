import pandas as pd
from _01_sources.bybit_client import get_ohlcv
from _00_config import config


def run_etl():
    raw_data = get_ohlcv(config.TRADING_PAIR, config.TIMEFRAME)

    df = pd.DataFrame(raw_data, columns=[
        'timestamp',  # Время открытия свечи (в миллисекундах)
        'open',       # Цена открытия
        'high',       # Максимальная цена
        'low',        # Минимальная цена
        'close',      # Цена закрытия
        'volume',     # Объём торгов
        'turnover'    # Дополнительные данные (оборот)
    ])
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    df = df.sort_values('timestamp')
    df.to_csv(f"{config.DATA_PATH}{config.TRADING_PAIR}_{config.TIMEFRAME}.csv", index=False)
     
  
    print(f"Данные сохранены: {config.DATA_PATH}{config.TRADING_PAIR}_{config.TIMEFRAME}.csv")
 

if __name__ == "__main__":
    run_etl()