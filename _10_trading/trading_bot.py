import time  # Импортируем модуль для создания задержек между итерациями цикла
from _03_datasets.dataset_manager import DatasetManager  # Импортируем менеджер для работы с датасетами
from _04_indicators.ema_calculator import calculate_ema
from _04_indicators.rci_calculator import calculate_rsi  # Импорт функции расчёта EMA
from _05_patterns.ema_crossover_strategy import detect_ema_crossover_signals  # Импорт стратегии поиска сигналов
from _05_patterns.rsi_strategy import detect_rsi_signal
from _07_management.risk_manager import calculate_position_size, calculate_sl_tp  # Импорт функций риск-менеджмента
from _01_sources.bybit_client import session  # Импорт сессии подключения к API ByBit
from _00_config import config  # Импорт конфигурационных параметров проекта
 
def run_trading_bot():
    """
    Основной цикл работы торгового бота.
    Здесь происходит получение данных, анализ и отправка ордеров.
    """
    balance = 1000  # Устанавливаем стартовый баланс (в реальном боте получаем с биржи)
 
    # Инициализируем менеджер данных для выбранной торговой пары и таймфрейма
    dm = DatasetManager(config.TRADING_PAIR, config.TIMEFRAME)
 
    while True:  # Запускаем бесконечный цикл для постоянной работы бота
        dm.refresh_data()  # Обновляем данные (запуск ETL и загрузка актуальных свечей)
        df = dm.get_latest_data(50).copy().reset_index(drop=True)  # Получаем последние 50 свечей для анализа
        # Определяем торговые сигналы на основе пересечения EMA
        df = detect_ema_crossover_signals(df, short_period=9, long_period=21)
        df = detect_rsi_signal(df, overbought=70, oversold=30)
        # Получаем последний сигнал (на текущей свече)
        """Тут получается следующее:
            - надо создать счетчик: Условно три индикатора если на покупку/продажу будет 2 из 3, то мы покупаем/продаем"""
        last_signal = sum(df[['signal_ema', 'signal_rsi']].iloc[-1])        
        if last_signal > 1 or last_signal < -1:  # Если есть сигнал (1 = Buy, -1 = Sell)
            current_price = df['close'].iloc[-1]  # Получаем текущую цену актива
            position_size = calculate_position_size(balance, current_price)  # Рассчитываем безопасный объем сделки
            sl, tp = calculate_sl_tp(current_price)  # Рассчитываем уровни стоп-лосса и тейк-профита
 
            # Отправляем рыночный ордер на биржу ByBit через API
            order = session.place_order(
                category="linear",  # Тип рынка (фьючерсы)
                symbol=config.TRADING_PAIR,  # Торговая пара
                side="Buy" if last_signal == 2 else "Sell",  # Направление сделки в зависимости от сигнала
                orderType="Market",  # Рыночный ордер
                qty=position_size,  # Количество актива
                stopLoss=sl,  # Уровень стоп-лосса
                takeProfit=tp  # Уровень тейк-профита
            )
 
            # Выводим информацию об отправленном ордере
            print(f"Отправлен ордер: {order}")
        else:
            # Если сигнала нет, бот просто ждет следующей проверки
            print("Сигнала нет. Ожидание следующего цикла...")
 
        time.sleep(60)  # Пауза на 60 секунд перед следующей итерацией (зависит от таймфрейма стратегии)
 
# Точка входа для запуска бота
if __name__ == "__main__":
    run_trading_bot()  # Запуск основного цикла торгового бота


