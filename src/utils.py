import pandas as pd
from datetime import datetime


def get_greeting(current_time: datetime) -> str:
    """
    Get greeting based on the current time.

    Args:
        current_time (datetime): The current time.

    Returns:
        str: The greeting string.
    """
    if 5 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards_info(data: pd.DataFrame) -> list:
    """
    Get cards information from the transaction data.

    Args:
        data (pd.DataFrame): The transaction data.

    Returns:
        list: List of dictionaries with cards information.
    """
    cards = data.groupby('Номер карты').agg({'Сумма операции': 'sum'}).reset_index()
    cards['Кэшбэк'] = cards['Сумма операции'] * 0.01
    result = []
    for _, row in cards.iterrows():
        result.append({
            "last_digits": row['Номер карты'],
            "total_spent": row['Сумма операции'],
            "cashback": row['Кэшбэк']
        })
    return result


def get_top_transactions(data: pd.DataFrame) -> list:
    """
    Get top transactions by payment amount.

    Args:
        data (pd.DataFrame): The transaction data.

    Returns:
        list: List of dictionaries with top transactions.
    """
    top_transactions = data.sort_values(by='Сумма платежа', ascending=False).head(5)
    result = []
    for _, row in top_transactions.iterrows():
        result.append({
            "Дата операции": row['Дата операции'].strftime('%Y-%m-%d %H:%M:%S'),
            "Сумма платежа": row['Сумма платежа'],
            "Категория": row['Категория'],
            "Описание": row['Описание']
        })
    return result


def get_currency_rates() -> list:
    """
    Get current currency rates.

    Returns:
        list: List of dictionaries with currency rates.
    """
    return [
        {"currency": "USD", "rate": 73.21},
        {"currency": "EUR", "rate": 87.08}
    ]


def get_stock_prices() -> list:
    """
    Get current stock prices.

    Returns:
        list: List of dictionaries with stock prices.
    """
    return [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08}
    ]
