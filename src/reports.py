import pandas as pd
import json


def expenses_by_category():
    """
    Calculate expenses by category for the last three months.

    Args:
        transactions (pd.DataFrame): DataFrame with transaction data.
        category (str): Category for which to calculate expenses.
        date (str, optional): Reference date (default: None, uses current date).

    Returns:
        pd.DataFrame: DataFrame with calculated expenses.
    """
    # ваш код


def expenses_by_day_of_week(date=None):
    """
    Calculate average expenses by day of the week for the last three months.

    Args:
        transactions (pd.DataFrame): DataFrame with transaction data.
        date (str, optional): Reference date (default: None, uses current date).

    Returns:
        pd.DataFrame: DataFrame with calculated average expenses by day of the week.
    """
    # ваш код


def expenses_by_workday_weekend(transactions, date=None):
    """
    Calculate average expenses for workdays and weekends for the last three months.

    Args:
        transactions (pd.DataFrame): DataFrame with transaction data.
        date (str, optional): Reference date (default: None, uses current date).

    Returns:
        pd.DataFrame: DataFrame with calculated average expenses for workdays and weekends.
    """
    # ваш код


def expenses_by_category(data, year, month):
    """
    Фильтрует данные за указанный месяц и год и возвращает суммы расходов по категориям.

    :param data: DataFrame с данными транзакций
    :param year: Год для фильтрации данных
    :param month: Месяц для фильтрации данных
    :return: JSON строка с суммами расходов по категориям
    """
    data["Дата операции"] = pd.to_datetime(data["Дата операции"])
    filtered_data = data[
        (data["Дата операции"].dt.year == year)
        & (data["Дата операции"].dt.month == month)
        ]

    expenses_by_category = (
        filtered_data.groupby("Категория")["Сумма платежа"].sum().reset_index()
    )
    result = expenses_by_category.set_index("Категория")["Сумма платежа"].to_dict()
    return json.dumps(result, ensure_ascii=False, indent=4)


def expenses_by_day_of_week(data, year, month):
    """
    Фильтрует данные за указанный месяц и год и возвращает суммы расходов по дням недели.

    :param data: DataFrame с данными транзакций
    :param year: Год для фильтрации данных
    :param month: Месяц для фильтрации данных
    :return: JSON строка с суммами расходов по дням недели
    """
    data["Дата операции"] = pd.to_datetime(data["Дата операции"])
    filtered_data = data[
        (data["Дата операции"].dt.year == year)
        & (data["Дата операции"].dt.month == month)
        ]

    expenses_by_day_of_week = (
        filtered_data.groupby(filtered_data["Дата операции"].dt.dayofweek)[
            "Сумма платежа"
        ]
        .sum()
        .reset_index()
    )
    result = expenses_by_day_of_week.set_index("Дата операции")[
        "Сумма платежа"
    ].to_dict()
    return json.dumps(result, ensure_ascii=False, indent=4)


def expenses_by_workday_weekend(data, year, month):
    """
    Фильтрует данные за указанный месяц и год и возвращает суммы расходов по рабочим и выходным дням.

    :param data: DataFrame с данными транзакций
    :param year: Год для фильтрации данных
    :param month: Месяц для фильтрации данных
    :return: JSON строка с суммами расходов по рабочим и выходным дням
    """
    data["Дата операции"] = pd.to_datetime(data["Дата операции"])
    filtered_data = data[
        (data["Дата операции"].dt.year == year)
        & (data["Дата операции"].dt.month == month)
        ]

    filtered_data["Рабочий день"] = filtered_data["Дата операции"].dt.dayofweek < 5
    expenses_by_workday_weekend = (
        filtered_data.groupby("Рабочий день")["Сумма платежа"].sum().reset_index()
    )
    expenses_by_workday_weekend["Рабочий день"] = expenses_by_workday_weekend[
        "Рабочий день"
    ].map({True: "Рабочий день", False: "Выходной день"})

    result = expenses_by_workday_weekend.set_index("Рабочий день")[
        "Сумма платежа"
    ].to_dict()
    return json.dumps(result, ensure_ascii=False, indent=4)


def expenses_by_hour(data, year, month):
    """
    Фильтрует данные за указанный месяц и год и возвращает суммы расходов по часам дня.

    :param data: DataFrame с данными транзакций
    :param year: Год для фильтрации данных
    :param month: Месяц для фильтрации данных
    :return: JSON строка с суммами расходов по часам дня
    """
    data["Дата операции"] = pd.to_datetime(data["Дата операции"])
    filtered_data = data[
        (data["Дата операции"].dt.year == year)
        & (data["Дата операции"].dt.month == month)
        ]

    expenses_by_hour = (
        filtered_data.groupby(filtered_data["Дата операции"].dt.hour)["Сумма платежа"]
        .sum()
        .reset_index()
    )
    result = expenses_by_hour.set_index("Дата операции")["Сумма платежа"].to_dict()
    return json.dumps(result, ensure_ascii=False, indent=4)
