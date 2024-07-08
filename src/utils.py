from datetime import datetime

import pandas as pd


def get_greeting(current_time: datetime) -> str:
    if 5 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards_info(data: pd.DataFrame) -> list:
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
    return [
        {"currency": "USD", "rate": 73.21},
        {"currency": "EUR", "rate": 87.08}
    ]


def get_stock_prices() -> list:
    return [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08}
    ]


def analyze_transactions(data: pd.DataFrame, date: datetime, period: str) -> tuple:
    """
    Analyze transactions and return expenses and income.

    Args:
        data (pd.DataFrame): The transaction data.
        date (datetime): The date for analysis.
        period (str): The period for analysis (W, M, Y, ALL).

    Returns:
        tuple: A tuple containing expenses and income data.
    """
    if period == 'W':
        start_date = date - pd.Timedelta(days=date.weekday())
    elif period == 'M':
        start_date = date.replace(day=1)
    elif period == 'Y':
        start_date = date.replace(month=1, day=1)
    else:
        start_date = data['Дата операции'].min()

    filtered_data = data[(data['Дата операции'] >= start_date) & (data['Дата операции'] <= date)]

    expenses = filtered_data[filtered_data['Сумма платежа'] < 0].copy()
    income = filtered_data[filtered_data['Сумма платежа'] > 0].copy()

    expenses_total = expenses['Сумма платежа'].sum()
    income_total = income['Сумма платежа'].sum()

    main_expenses = expenses.groupby('Категория').agg({'Сумма платежа': 'sum'}).reset_index()
    main_expenses = main_expenses.nlargest(7, 'Сумма платежа')
    other_expenses = expenses[~expenses['Категория'].isin(main_expenses['Категория'])]['Сумма платежа'].sum()
    main_expenses = main_expenses.append({'Категория': 'Остальное', 'Сумма платежа': other_expenses},
                                         ignore_index=True)

    transfers_and_cash = expenses[expenses['Категория'].isin(['Наличные', 'Переводы'])].copy()

    main_income = income.groupby('Категория').agg({'Сумма платежа': 'sum'}).reset_index()

    return {
        'total_amount': round(expenses_total),
        'main': main_expenses.to_dict(orient='records'),
        'transfers_and_cash': transfers_and_cash.to_dict(orient='records')
    }, {
        'total_amount': round(income_total),
        'main': main_income.to_dict(orient='records')
    }
