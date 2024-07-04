import pytest
import pandas as pd
import json
from datetime import datetime
from src.reports import (
    expenses_by_category,
    expenses_by_day_of_week,
    expenses_by_workday_weekend,
    expenses_by_hour,
)


@pytest.fixture
def sample_data():
    data = {
        "Дата операции": [
            datetime(2021, 12, 31, 16, 44),
            datetime(2021, 12, 15, 16, 42),
            datetime(2021, 11, 30, 16, 39),
            datetime(2021, 12, 25, 12, 0),
        ],
        "Категория": [
            "Супермаркеты",
            "Супермаркеты",
            "Различные товары",
            "Развлечения",
        ],
        "Сумма платежа": [64.0, 160.89, 200.0, 50.0],
    }
    return pd.DataFrame(data)


def test_expenses_by_category(sample_data):
    year = 2021
    month = 12
    response = expenses_by_category(sample_data, year, month)

    response_dict = json.loads(response)

    assert "Супермаркеты" in response_dict
    assert response_dict["Супермаркеты"] == 224.89
    assert "Различные товары" not in response_dict


def test_expenses_by_day_of_week(sample_data):
    year = 2021
    month = 12
    response = expenses_by_day_of_week(sample_data, year, month)

    response_dict = json.loads(response)

    # Преобразуем ключи в целые числа
    response_dict = {int(k): v for k, v in response_dict.items()}

    # Проверка, что расходы распределены по дням недели
    assert 2 in response_dict  # Среда
    assert 4 in response_dict  # Пятница


def test_expenses_by_workday_weekend(sample_data):
    year = 2021
    month = 12
    response = expenses_by_workday_weekend(sample_data, year, month)

    response_dict = json.loads(response)

    assert "Рабочий день" in response_dict
    assert "Выходной день" in response_dict


def test_expenses_by_hour(sample_data):
    year = 2021
    month = 12
    response = expenses_by_hour(sample_data, year, month)

    response_dict = json.loads(response)

    # Преобразуем ключи в целые числа
    response_dict = {int(k): v for k, v in response_dict.items()}

    assert 16 in response_dict  # 16-й час
