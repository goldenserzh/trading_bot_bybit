import pandas as pd
from _00_config import config
import talib as pta


def calculate_rsi(df):
    df['RSI'] = pta.RSI(df['close'], timeperiod=15)

    return df


if __name__ == '__main__':
    df = pd.read_csv('_03_datasets/BTCUSDT_15.csv')
    df = calculate_rsi(df)
    df.to_csv(f"{config.DATA_PATH}{config.TRADING_PAIR}_{config.TIMEFRAME}.csv", index=False)
    print(df)