from pybit.unified_trading import HTTP
from _00_config import config

# Создание сессии (запрос на bybit)
session = HTTP(
    api_key=config.BYBIT_API_KEY,
    api_secret=config.BYBIT_API_SECRET,
    testnet=(config.MODE == "paper")
)

#Получаение данных по свечам
def get_ohlcv(symbol, interval, limit=200 ): #лимит - кол-во свечей для получения с биржы
    response = session.get_kline(
        category="linear",
        symbol=symbol, 
        interval=interval,
        limit=limit
    )
    return response['result']['list']
 
# Пример вызова
if __name__ == "__main__":
    data = get_ohlcv(config.TRADING_PAIR, config.TIMEFRAME)
    print(data[:2])