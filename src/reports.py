import json
import pandas as pd
from datetime import datetime, timedelta
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def expenses_by_category(data: pd.DataFrame, category: str, date: str = None) -> str:
    """
    Calculate expenses by category for the last three months from the given date.

    Args:
        data (pd.DataFrame): The transaction data.
        category (str): The category to filter.
        date (str): The end date for the three-month period (format 'YYYY-MM-DD'). Defaults to current date.

    Returns:
        str: A JSON string with the total expenses by category for the specified period.
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    end_date = datetime.strptime(date, '%Y-%m-%d')
    start_date = end_date - timedelta(days=90)

    logger.info(f"Calculating expenses for category '{category}' from {start_date.date()} to {end_date.date()}")

    filtered_data = data[
        (data['Дата операции'] >= start_date) &
        (data['Дата операции'] <= end_date) &
        (data['Категория'] == category)
        ]
    total_expenses = filtered_data['Сумма платежа'].sum()

    result = {
        "category": category,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "total_expenses": total_expenses
    }

    logger.info(
        f"Total expenses for category '{category}' from {start_date.date()} to {end_date.date()}: {total_expenses}")

    return json.dumps(result, ensure_ascii=False, indent=4)


def expenses_by_day_of_week(data: pd.DataFrame, year: int, month: int) -> str:
    """
    Calculate expenses by day of the week for the given month and year.

    Args:
        data (pd.DataFrame): The transaction data.
        year (int): The year for analysis.
        month (int): The month for analysis.

    Returns:
        str: A JSON string with the total expenses by day of the week.
    """
    logger.info(f"Calculating expenses by day of the week for {year}-{month:02d}")

    filtered_data = data[
        (data['Дата операции'].dt.year == year) &
        (data['Дата операции'].dt.month == month)
        ]
    filtered_data['day_of_week'] = filtered_data['Дата операции'].dt.dayofweek
    expenses_by_day = filtered_data.groupby('day_of_week')['Сумма платежа'].sum().to_dict()

    result = {
        "year": year,
        "month": month,
        "expenses_by_day_of_week": expenses_by_day
    }

    logger.info(f"Expenses by day of the week for {year}-{month:02d}: {expenses_by_day}")

    return json.dumps(result, ensure_ascii=False, indent=4)


def expenses_by_workday_weekend(data: pd.DataFrame, year: int, month: int) -> str:
    """
    Calculate expenses by workday and weekend for the given month and year.

    Args:
        data (pd.DataFrame): The transaction data.
        year (int): The year for analysis.
        month (int): The month for analysis.

    Returns:
        str: A JSON string with the total expenses by workday and weekend.
    """
    logger.info(f"Calculating expenses by workday and weekend for {year}-{month:02d}")

    filtered_data = data[
        (data['Дата операции'].dt.year == year) &
        (data['Дата операции'].dt.month == month)
        ]
    filtered_data['is_workday'] = filtered_data['Дата операции'].dt.dayofweek < 5
    workday_expenses = filtered_data[filtered_data['is_workday']]['Сумма платежа'].sum()
    weekend_expenses = filtered_data[~filtered_data['is_workday']]['Сумма платежа'].sum()

    result = {
        "year": year,
        "month": month,
        "workday_expenses": workday_expenses,
        "weekend_expenses": weekend_expenses
    }

    logger.info(
        f"Expenses by workday and weekend for {year}-{month:02d}: "
        f"workday={workday_expenses}, weekend={weekend_expenses}"
    )

    return json.dumps(result, ensure_ascii=False, indent=4)


def expenses_by_hour_func(data: pd.DataFrame, year: int, month: int) -> str:
    """
    Calculate expenses by hour for the given month and year.

    Args:
        data (pd.DataFrame): The transaction data.
        year (int): The year for analysis.
        month (int): The month for analysis.

    Returns:
        str: A JSON string with the total expenses by hour.
    """
    logger.info(f"Calculating expenses by hour for {year}-{month:02d}")

    filtered_data = data[
        (data['Дата операции'].dt.year == year) &
        (data['Дата операции'].dt.month == month)
        ]
    filtered_data['hour'] = filtered_data['Дата операции'].dt.hour
    expenses_by_hour = filtered_data.groupby('hour')['Сумма платежа'].sum().to_dict()

    result = {
        "year": year,
        "month": month,
        "expenses_by_hour": expenses_by_hour
    }

    logger.info(f"Expenses by hour for {year}-{month:02d}: {expenses_by_hour}")

    return json.dumps(result, ensure_ascii=False, indent=4)
