import pandas as pd
import matplotlib.pyplot as plt
from _05_patterns.ema_crossover_strategy import detect_ema_crossover_signals
from _05_patterns.rsi_strategy import detect_rsi_signal
def plot_ema_signals(df, short_period=9, long_period=21):
    """
    Функция для построения графика цены с наложенными EMA и торговыми сигналами.
 
    :param df: DataFrame с колонками ['timestamp', 'close', 'EMA_xx', 'signal']
    :param short_period: Период короткой EMA
    :param long_period: Период длинной EMA
    """
    plt.figure(figsize=(14, 7))  # Размер графика
 
    # Строим линию цены (close)
    plt.plot(df['timestamp'], df['close'], label='Close Price', linewidth=1)
 
    # Строим EMA линии
    plt.plot(df['timestamp'], df[f'EMA_{short_period}'], label=f'EMA {short_period}', linestyle='--')
    plt.plot(df['timestamp'], df[f'EMA_{long_period}'], label=f'EMA {long_period}', linestyle='--')
 
    # Добавляем точки входа и выхода
    df['general_signal'] = df['signal_ema'] + df['signal_rsi']
    buy_signals = df[df['general_signal'] == 1]
    sell_signals = df[df['signal_ema'] == -1]
    
    # Отмечаем buy сигналы зелёными треугольниками
    plt.scatter(buy_signals['timestamp'], buy_signals['close'], marker='^', color='green', label='Buy Signal', s=100)
 
    # Отмечаем sell сигналы красными перевёрнутыми треугольниками
    plt.scatter(sell_signals['timestamp'], sell_signals['close'], marker='v', color='red', label='Sell Signal', s=100)
 
    # Настройки графика
    plt.title(f"Торговые сигналы по стратегии EMA Crossover ({short_period}/{long_period})")
    plt.xlabel('Время')
    plt.ylabel('Цена')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
 
    # Показываем график
    plt.show()
 
# # Пример использования
if __name__ == "__main__":
    # Загружаем датасет с рассчитанными EMA и сигналами
    df = pd.read_csv('./_03_datasets/BTCUSDT_15.csv', parse_dates=['timestamp'])
    df = detect_ema_crossover_signals(df)
    df = detect_rsi_signal(df)
    # Строим график
    plot_ema_signals(df, short_period=9, long_period=21)