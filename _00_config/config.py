from dotenv import load_dotenv
import os

load_dotenv()

BYBIT_API_KEY =os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

TRADING_PAIR = "BTCUSDT"
TIMEFRAME =  '15'

EMA_SHORT = 9
EMA_LONG = 21

MAX_TRADE_SIZE_PERCENT = 0.05
STOP_LOSS_PERCENT = 1.5
TAKE_PROFIT_PERCENT = 3.0

MODE = 'live' #также можжно live - цена в реальном времени, paper - историчяеские данные

DATA_PATH = "./_03_datasets/"
LOG_PATH = "./logs/"

