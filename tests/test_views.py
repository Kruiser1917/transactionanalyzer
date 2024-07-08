import json


import pandas as pd
import pytest

from src.views import events_page, main_page


@pytest.fixture
def sample_data():
    data = {
        'Дата операции': [
            '2021-12-31 16:44:00',
            '2021-12-15 16:42:00',
            '2021-11-30 16:39:00',
            '2021-10-31 12:00:00',
            '2021-12-25 12:00:00'
        ],
        'Номер карты': [
            '1111222233334444',
            '1111222233334444',
            '5555666677778888',
            '9999000011112222',
            '1111222233334444'
        ],
        'Статус': [
            'OK', 'OK', 'FAILED', 'OK', 'OK'
        ],
        'Сумма операции': [
            100.00, 200.00, 300.00, 400.00, 500.00
        ],
        'Валюта операции': [
            'RUB', 'RUB', 'RUB', 'RUB', 'RUB'
        ],
        'Сумма платежа': [
            64.00, 160.89, 200.00, 50.00, 100.00
        ],
        'Валюта платежа': [
            'RUB', 'RUB', 'RUB', 'RUB', 'RUB'
        ],
        'Кэшбэк': [
            1, 2, 3, 4, 5
        ],
        'Категория': [
            'Супермаркеты', 'Супермаркеты', 'Различные товары', 'Развлечения', 'Супермаркеты'
        ],
        'MCC': [
            '5411', '5411', '5999', '7999', '5411'
        ],
        'Описание': [
            'Магнит', 'Магнит', 'Лента', 'Кино', 'Магнит'
        ],
        'Бонусы (включая кешбэк)': [
            1, 2, 3, 4, 5
        ],
        'Округление на "Инвесткопилку"': [
            2, 3, 4, 5, 6
        ],
        'Сумма операции с округлением': [
            66.00, 163.89, 204.00, 55.00, 106.00
        ]
    }
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])
    return df


def test_main_page(sample_data):
    current_time_str = '2021-12-31 16:00:00'
    response = main_page(sample_data, current_time_str)

    response_dict = json.loads(response)

    assert 'greeting' in response_dict
    assert 'cards' in response_dict
    assert 'top_transactions' in response_dict
    assert 'currency_rates' in response_dict
    assert 'stock_prices' in response_dict


def test_events_page(sample_data):
    date_str = '2021-12-31'
    period = 'M'
    response = events_page(sample_data, date_str, period)

    response_dict = json.loads(response)

    assert 'expenses' in response_dict
    assert 'income' in response_dict
    assert 'currency_rates' in response_dict
    assert 'stock_prices' in response_dict
