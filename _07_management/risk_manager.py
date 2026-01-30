
from _00_config import config
 
def calculate_position_size(balance, price):
    #тут надо подумтаь над тем, как разделить на равное кол-во сделок, а не сразу
    #по сути мы можем сделать след образом: пока цена, которой мы можем пожертвовать не < какому то числу то выполняем расчеты
    """
    Рассчитываем размер позиции на основе баланса и настроек риска.
 
    :param balance: Текущий баланс в USDT
    :param price: Текущая цена актива
    :return: Размер позиции в BTC (или другом активе)
    """
    # Ограничение: максимальный процент от баланса в одной сделке
    risk_usdt = balance * (config.MAX_TRADE_SIZE_PERCENT / 100)
 
    # Конвертируем сумму в количество актива
    position_size = risk_usdt / price
 
    return round(position_size, 6)  # Округляем до 6 знаков (актуально для крипты)
 
def calculate_sl_tp(entry_price): # стоп лоссы надо подробнее разобрать
    """
    Рассчитываем уровни стоп-лосса и тейк-профита.
 
    :param entry_price: Цена входа в сделку
    :return: Кортеж (stop_loss_price, take_profit_price)
    """
    stop_loss = entry_price * (1 - config.STOP_LOSS_PERCENT / 100)
    take_profit = entry_price * (1 + config.TAKE_PROFIT_PERCENT / 100)
 
    return round(stop_loss, 2), round(take_profit, 2)
 
# Пример использования
if __name__ == "__main__":
    current_balance = 1000  # Допустим, у нас 1000 USDT
    current_price = 30000   # Цена BTC
 
    # Расчёт размера позиции
    size = calculate_position_size(current_balance, current_price)
    print(f"Рекомендованный размер позиции: {size} BTC")
 
    # Расчёт уровней SL и TP
    sl, tp = calculate_sl_tp(current_price)
    print(f"Stop Loss: {sl} USDT, Take Profit: {tp} USDT")