import pandas as pd
from datetime import datetime
import json


def get_greeting(current_time):
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def main_page(data, current_time_str):
    current_time = datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(current_time)

    # Process data for cards
    cards = []
    for card, group in data.groupby("Номер карты"):
        total_spent = group["Сумма платежа"].sum()
        cashback = total_spent / 100  # Assuming 1% cashback
        cards.append(
            {
                "last_digits": card[-4:],
                "total_spent": round(total_spent, 2),
                "cashback": round(cashback, 2),
            }
        )

    # Ensure 'Дата операции' is in datetime format
    data["Дата операции"] = pd.to_datetime(data["Дата операции"])

    # Get top 5 transactions from the entire dataset
    top_transactions = data.nlargest(5, "Сумма платежа")[
        ["Дата операции", "Сумма платежа", "Категория", "Описание"]
    ]
    top_transactions["Дата операции"] = top_transactions["Дата операции"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    top_transactions = top_transactions.to_dict(orient="records")

    # Placeholder for currency rates and stock prices
    currency_rates = [
        {"currency": "USD", "rate": 73.21},
        {"currency": "EUR", "rate": 87.08},
    ]
    stock_prices = [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08},
    ]

    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(response, ensure_ascii=False, indent=4)


def events_page(data, current_time_str, period="M"):
    current_time = datetime.strptime(current_time_str, "%Y-%m-%d")
    if period == "W":
        start_date = current_time - pd.DateOffset(weeks=1)
    elif period == "M":
        start_date = current_time - pd.DateOffset(months=1)
    elif period == "Y":
        start_date = current_time - pd.DateOffset(years=1)
    elif period == "ALL":
        start_date = data["Дата операции"].min()
    else:
        start_date = current_time - pd.DateOffset(months=1)

    # Ensure 'Дата операции' is in datetime format
    data["Дата операции"] = pd.to_datetime(data["Дата операции"])

    period_data = data[
        (data["Дата операции"] >= start_date) & (data["Дата операции"] <= current_time)
    ]

    expenses_total = period_data["Сумма платежа"].sum()
    income_total = period_data["Сумма операции"].sum()

    main_expenses = (
        period_data.groupby("Категория")["Сумма платежа"]
        .sum()
        .nlargest(7)
        .reset_index()
    )
    other_expenses = period_data[
        ~period_data["Категория"].isin(main_expenses["Категория"])
    ]["Сумма платежа"].sum()
    main_expenses = pd.concat(
        [
            main_expenses,
            pd.DataFrame(
                {"Категория": ["Остальное"], "Сумма платежа": [other_expenses]}
            ),
        ],
        ignore_index=True,
    )

    transfers_and_cash = (
        period_data[period_data["Категория"].isin(["Наличные", "Переводы"])]
        .groupby("Категория")["Сумма платежа"]
        .sum()
        .reset_index()
    )

    main_income = (
        period_data.groupby("Категория")["Сумма операции"]
        .sum()
        .nlargest(7)
        .reset_index()
    )

    response = {
        "expenses": {
            "total_amount": round(expenses_total, 2),
            "main": main_expenses.to_dict(orient="records"),
            "transfers_and_cash": transfers_and_cash.to_dict(orient="records"),
        },
        "income": {
            "total_amount": round(income_total, 2),
            "main": main_income.to_dict(orient="records"),
        },
        "currency_rates": [
            {"currency": "USD", "rate": 73.21},
            {"currency": "EUR", "rate": 87.08},
        ],
        "stock_prices": [
            {"stock": "AAPL", "price": 150.12},
            {"stock": "AMZN", "price": 3173.18},
            {"stock": "GOOGL", "price": 2742.39},
            {"stock": "MSFT", "price": 296.71},
            {"stock": "TSLA", "price": 1007.08},
        ],
    }

    return json.dumps(response, ensure_ascii=False, indent=4)
