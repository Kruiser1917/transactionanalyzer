import json
import pandas as pd
from datetime import datetime
from src.utils import get_greeting, get_cards_info, get_top_transactions, get_currency_rates, get_stock_prices


def main_page(data: pd.DataFrame, current_time_str: str) -> str:
    """
    Generate JSON response for the main page.

    Args:
        data (pd.DataFrame): The transaction data.
        current_time_str (str): The current time as a string.

    Returns:
        str: JSON string with the response data.
    """
    current_time = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M:%S')
    greeting = get_greeting(current_time)
    cards = get_cards_info(data)
    top_transactions = get_top_transactions(data)
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()

    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    return json.dumps(response, ensure_ascii=False, indent=4)


def events_page(data: pd.DataFrame, date_str: str, period: str) -> str:
    """
    Generate JSON response for the events page.

    Args:
        data (pd.DataFrame): The transaction data.
        date_str (str): The date as a string.
        period (str): The period for analysis (W, M, Y, ALL).

    Returns:
        str: JSON string with the response data.
    """
    date = datetime.strptime(date_str, '%Y-%m-%d')
    expenses, income = analyze_transactions(data, date, period)
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()

    response = {
        "expenses": expenses,
        "income": income,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    return json.dumps(response, ensure_ascii=False, indent=4)
