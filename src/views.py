import json
from datetime import datetime

import pandas as pd

from src.utils import (
    analyze_transactions,
    get_cards_info,
    get_currency_rates,
    get_greeting,
    get_stock_prices,
    get_top_transactions,
)


def main_page(data: pd.DataFrame, current_time_str: str) -> str:
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
