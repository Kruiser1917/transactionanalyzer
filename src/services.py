# src/services.py

import json


def analyze_cashback(data, year, month):
    """
    Analyze the most profitable cashback categories for a given month and year.

    Args:
        data (pd.DataFrame): DataFrame with transaction data.
        year (int): Year for the analysis.
        month (int): Month for the analysis.

    Returns:
        str: JSON response with analysis results.
    """
    # ваш код


def analyze_investment(data, year, month):
    """
    Calculate the total amount of money saved through investment rounding.

    Args:
        data (pd.DataFrame): DataFrame with transaction data.
        year (int): Year for the analysis.
        month (int): Month for the analysis.

    Returns:
        str: JSON response with total investment amount.
    """
    # ваш код


def simple_search(data, query):
    """
    Perform a simple search for transactions containing the query in description or category.

    Args:
        data (pd.DataFrame): DataFrame with transaction data.
        query (str): Search query.

    Returns:
        str: JSON response with search results.
    """
    # ваш код


def phone_number_search(data, phone_number):
    """
    Search for transactions containing the specified phone number in the description.

    Args:
        data (pd.DataFrame): DataFrame with transaction data.
        phone_number (str): Phone number to search for.

    Returns:
        str: JSON response with search results.
    """
    # ваш код


def individual_transfers_search(data, individual_name):
    """
    Search for transactions that are transfers to individuals.

    Args:
        data (pd.DataFrame): DataFrame with transaction data.
        individual_name (str): Name of the individual to search for.

    Returns:
        str: JSON response with search results.
    """
    # ваш код


def analyze_cashback_categories(data, year, month):
    filtered_data = data[(data['Дата операции'].dt.year == year) & (data['Дата операции'].dt.month == month)]
    cashback_by_category = filtered_data.groupby('Категория')['Кэшбэк'].sum()
    result = cashback_by_category.to_dict()
    return json.dumps(result, ensure_ascii=False, indent=4)


def analyze_investment(data, year, month):
    filtered_data = data[(data['Дата операции'].dt.year == year) & (data['Дата операции'].dt.month == month)]
    total_investment = filtered_data['Инвесткопилка'].sum()
    result = {
        'year': year,
        'month': month,
        'total_investment': int(total_investment)  # Преобразуем в int для корректной сериализации
    }
    return json.dumps(result, ensure_ascii=False, indent=4)


def simple_search(data, query):
    filtered_data = data[data['Описание'].str.contains(query, na=False)]
    result = filtered_data.to_dict(orient='records')
    for record in result:
        record['Дата операции'] = record['Дата операции'].strftime('%Y-%m-%d %H:%M:%S')  # Преобразуем в строку
    return json.dumps(result, ensure_ascii=False, indent=4)


def phone_number_search(data, phone_number):
    filtered_data = data[data['Описание'].str.contains(phone_number, na=False)]
    result = filtered_data.to_dict(orient='records')
    for record in result:
        record['Дата операции'] = record['Дата операции'].strftime('%Y-%m-%d %H:%M:%S')  # Преобразуем в строку
    return json.dumps(result, ensure_ascii=False, indent=4)


def individual_transfers_search(data, individual_name):
    filtered_data = data[data['Описание'].str.contains(individual_name, na=False)]
    result = filtered_data.to_dict(orient='records')
    for record in result:
        record['Дата операции'] = record['Дата операции'].strftime('%Y-%m-%d %H:%M:%S')  # Преобразуем в строку
    return json.dumps(result, ensure_ascii=False, indent=4)
