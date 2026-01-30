import dash  # Фреймворк для создания веб-дашбордов
from dash import html, dcc  # Компоненты интерфейса
import plotly.graph_objs as go  # Для построения графиков
import pandas as pd  # Работа с данными
from datetime import datetime, timedelta  # Для генерации временных меток
import numpy as np  # Для создания тестовых данных
 
# --- Генерация тестовых данных для примера ---
dates = [datetime.now() - timedelta(minutes=15*i) for i in range(20)][::-1]  # Последние 20 точек времени
balances = np.cumsum(np.random.randn(20)) + 1000  # Симуляция баланса
 
df = pd.DataFrame({'time': dates, 'balance': balances})  # Создаем DataFrame
 
# --- Инициализация Dash-приложения ---
app = dash.Dash(__name__)
 
# --- Описание интерфейса дашборда ---
app.layout = html.Div(children=[
    html.H1(children='Trading Bot Dashboard', style={'textAlign': 'center'}),  # Заголовок
 
    html.Div(children=f"Статус бота: Активен", style={'textAlign': 'center', 'fontSize':20}),  # Статус бота
    html.Div(children=f"Текущий баланс: {df['balance'].iloc[-1]:.2f} USDT", style={'textAlign': 'center', 'fontSize':20}),  # Баланс
 
    # График изменения баланса
    dcc.Graph(
        id='balance-graph',
        figure={
            'data': [
                go.Scatter(
                    x=df['time'],
                    y=df['balance'],
                    mode='lines+markers',
                    name='Equity Curve'
                )
            ],
            'layout': go.Layout(
                title='Динамика Баланса',
                xaxis={'title': 'Время'},
                yaxis={'title': 'Баланс (USDT)'},
                template='plotly_dark'
            )
        }
    )
])
 
# --- Запуск сервера ---
if __name__ == '__main__':
    app.run(debug=True)