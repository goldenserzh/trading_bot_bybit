import pandas as pd
#ema, rsi
#[1,   1] -> buy


def general_signal(df: pd.DataFrame):
    df['gemneral_signal'] = df['signal_ema'] + df['signal_rsi']
    