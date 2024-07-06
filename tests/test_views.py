import pytest
import pandas as pd
import json
from datetime import datetime
from src.views import main_page, events_page


@pytest.fixture
def sample_data():
    data = {
        "Дата операции": [
            datetime(2021, 12, 31, 16, 44),
            datetime(2021, 12, 31, 16, 42),
            datetime(2021, 12, 31, 16, 39),
        ],
        "Дата платежа": [
            datetime(2021, 12, 31),
            datetime(2021, 12, 31),
            datetime(2021, 12, 31),
        ],
        "Номер карты": ["*7197", "*7197", "*5091"],
        "Статус": ["OK", "OK", "OK"],
        "Сумма операции": [-160.89, -64.00, -118.12],
        "Валюта операции": ["RUB", "RUB", "RUB"],
        "Сумма платежа": [-160.89, -64.00, -118.12],
        "Валюта платежа": ["RUB", "RUB", "RUB"],
        "Кэшбэк": [0, 0, 0],
        "Категория": ["Супермаркеты", "Супермаркеты", "Супермаркеты"],
        "MCC": [5411, 5411, 5411],
        "Описание": ["Колхоз", "Колхоз", "Магнит"],
        "Бонусы (включая кэшбэк)": [3, 1, 2],
        "Округление на инвесткопилку": [0, 0, 0],
        "Сумма операции с округлением": [160.89, 64.00, 118.12],
    }
    return pd.DataFrame(data)


def test_main_page(sample_data):
    current_time_str = "2021-12-31 16:00:00"
    response = main_page()

    assert "greeting" in response
    assert "cards" in response
    assert "top_transactions" in response
    assert "currency_rates" in response
    assert "stock_prices" in response

    response_dict = json.loads(response)

    assert response_dict["greeting"] == "Добрый день"
    assert len(response_dict["cards"]) == 2
    assert len(response_dict["top_transactions"]) == 3
    assert len(response_dict["currency_rates"]) == 2
    assert len(response_dict["stock_prices"]) == 5


def test_events_page(sample_data):
    current_time_str = "2021-12-31"
    response = events_page(current_time_str, period="M")

    assert "expenses" in response
    assert "income" in response
    assert "currency_rates" in response
    assert "stock_prices" in response

    response_dict = json.loads(response)

    assert "total_amount" in response_dict["expenses"]
    assert "main" in response_dict["expenses"]
    assert "transfers_and_cash" in response_dict["expenses"]
    assert "total_amount" in response_dict["income"]
    assert "main" in response_dict["income"]
    assert len(response_dict["currency_rates"]) == 2
    assert len(response_dict["stock_prices"]) == 5
