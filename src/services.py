# src/services.py

import json


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
