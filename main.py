"""
Главный скрипт для запуска торгового бота на ByBit.
Этот файл объединяет все модули и инициирует работу системы.
"""
 
import threading  # Для параллельного запуска дашборда и бота
# from _09_dashboard.dash_dashboard import app  # Импорт Dash-приложения
from _10_trading.trading_bot import run_trading_bot  # Импорт функции запуска торгового бота
from _09_dashboard.dash_dashboard import app
 
def start_dashboard():
    """
    Запуск веб-дашборда в отдельном потоке.
    """
    app.run_server(debug=False, use_reloader=False)  # Запуск Dash без режима перезагрузки
 
def start_bot():
    """
    Запуск торгового бота.
    """
    run_trading_bot()
 
if __name__ == "__main__":
    # Создаем поток для дашборда
    # dashboard_thread = threading.Thread(target=start_dashboard)
    # dashboard_thread.start()  # Запускаем дашборд
 
    # Запускаем бота в основном потоке
    start_bot()

print()