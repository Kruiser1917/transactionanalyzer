import json
import pandas as pd
import pytest
from src.reports import (
    expenses_by_category, expenses_by_day_of_week,
    expenses_by_workday_weekend, expenses_by_hour_func
)


@pytest.fixture
def sample_data():
    data = {
        'Дата операции': ['2021-12-31 16:44:00', '2021-12-15 16:42:00', '2021-11-30 16:39:00'],
        'Категория': ['Супермаркеты', 'Супермаркеты', 'Различные товары'],
        'Сумма платежа': [64.00, 160.89, 200.00]
    }
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])
    return df


def test_expenses_by_category(sample_data):
    category = 'Супермаркеты'
    result = expenses_by_category(sample_data, category, '2021-12-31')
    result_dict = json.loads(result)
    assert result_dict['category'] == category
    assert result_dict['total_expenses'] == 224.89


def test_expenses_by_day_of_week(sample_data):
    result = expenses_by_day_of_week(sample_data, 2021, 12)
    result_dict = json.loads(result)
    assert result_dict['expenses_by_day_of_week']['2'] == 160.89  # Wednesday
    assert result_dict['expenses_by_day_of_week']['4'] == 64.00  # Friday


def test_expenses_by_workday_weekend(sample_data):
    result = expenses_by_workday_weekend(sample_data, 2021, 12)
    result_dict = json.loads(result)
    assert result_dict['workday_expenses'] == 160.89
    assert result_dict['weekend_expenses'] == 64.00


def test_expenses_by_hour(sample_data):
    result = expenses_by_hour_func(sample_data, 2021, 12)
    result_dict = json.loads(result)
    assert result_dict['expenses_by_hour']['16'] == 224.89
