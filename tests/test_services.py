import json
from datetime import datetime

import pandas as pd
import pytest

from src.services import (
    analyze_cashback_categories,
    analyze_investment,
    individual_transfers_search,
    phone_number_search,
    simple_search,
)


@pytest.fixture
def sample_data():
    data = {
        'Дата операции': [datetime(2021, 12, 31, 16, 44), datetime(2021, 12, 15, 16, 42),
                          datetime(2021, 11, 30, 16, 39), datetime(2021, 12, 25, 12, 0)],
        'Категория': ['Супермаркеты', 'Супермаркеты', 'Различные товары', 'Развлечения'],
        'Кэшбэк': [10, 20, 30, 40],
        'Инвесткопилка': [5, 15, 25, 35],
        'Описание': ['Магнит', 'Пятерочка', 'Лента', '89123456789']
    }
    return pd.DataFrame(data)


def test_analyze_cashback_categories(sample_data):
    year = 2021
    month = 12
    response = analyze_cashback_categories(sample_data, year, month)

    response_dict = json.loads(response)

    assert response_dict['Супермаркеты'] == 30  # Предполагаемое значение для тестовых данных
    assert 'Различные товары' not in response_dict  # Для декабря 2021 данные по "Различные товары" не должны быть
    # учтены


def test_analyze_investment(sample_data):
    year = 2021
    month = 12
    response = analyze_investment(sample_data, year, month)

    response_dict = json.loads(response)

    assert response_dict['year'] == year
    assert response_dict['month'] == month
    assert response_dict['total_investment'] == 55  # Обновленное значение для тестовых данных


def test_simple_search(sample_data):
    query = 'Магнит'
    response = simple_search(sample_data, query)

    response_dict = json.loads(response)

    assert len(response_dict) == 1
    assert response_dict[0]['Описание'] == 'Магнит'


def test_phone_number_search(sample_data):
    phone_number = '89123456789'
    response = phone_number_search(sample_data, phone_number)

    response_dict = json.loads(response)

    assert len(response_dict) == 1  # Предполагаемое значение для тестовых данных
    assert response_dict[0]['Описание'] == phone_number


def test_individual_transfers_search(sample_data):
    individual_name = 'Иванов Иван'
    new_row = pd.DataFrame({
        'Дата операции': [datetime(2021, 12, 31, 16, 45)],
        'Категория': ['Переводы'],
        'Кэшбэк': [0],
        'Инвесткопилка': [0],
        'Описание': ['Перевод Иванов Иван']
    })
    sample_data = pd.concat([sample_data, new_row], ignore_index=True)
    response = individual_transfers_search(sample_data, individual_name)

    response_dict = json.loads(response)

    assert len(response_dict) == 1  # Предполагаемое значение для тестовых данных
    assert individual_name in response_dict[0]['Описание']
