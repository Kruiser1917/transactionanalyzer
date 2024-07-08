import json
import logging

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_investment(data: pd.DataFrame, year: int, month: int) -> str:
    """
    Analyze investment data and return total investment for the specified month and year.

    Args:
        data (pd.DataFrame): The transaction data.
        year (int): The year for analysis.
        month (int): The month for analysis.

    Returns:
        str: A JSON string with the total investment for the specified month and year.
    """
    logger.info(f"Analyzing investment data for {year}-{month:02d}")

    filtered_data = data[(data['Дата операции'].dt.year == year) & (data['Дата операции'].dt.month == month)]
    total_investment = filtered_data['Инвесткопилка'].sum()

    result = {
        "year": year,
        "month": month,
        "total_investment": total_investment
    }

    logger.info(f"Total investment for {year}-{month:02d}: {total_investment}")

    return json.dumps(result, ensure_ascii=False, indent=4)


def simple_search(data: pd.DataFrame, query: str) -> str:
    """
    Perform a simple search in the transaction data.

    Args:
        data (pd.DataFrame): The transaction data.
        query (str): The search query.

    Returns:
        str: A JSON string with the search results.
    """
    logger.info(f"Performing simple search for query: {query}")

    result = data[data['Описание'].str.contains(query, case=False, na=False)].to_dict(orient='records')

    logger.info(f"Found {len(result)} records matching query: {query}")

    return json.dumps(result, ensure_ascii=False, indent=4)


def phone_number_search(data: pd.DataFrame, phone_number: str) -> str:
    """
    Perform a search for transactions containing the specified phone number.

    Args:
        data (pd.DataFrame): The transaction data.
        phone_number (str): The phone number to search for.

    Returns:
        str: A JSON string with the search results.
    """
    result = data[data['Описание'].str.contains(phone_number, na=False)].to_dict(orient='records')
    return json.dumps(result, ensure_ascii=False, indent=4)


def individual_transfers_search(data: pd.DataFrame, individual_name: str) -> str:
    """
    Perform a search for transfers to individuals.

    Args:
        data (pd.DataFrame): The transaction data.
        individual_name (str): The name of the individual to search for.

    Returns:
        str: A JSON string with the search results.
    """
    result = data[data['Описание'].str.contains(individual_name, na=False)].to_dict(orient='records')
    return json.dumps(result, ensure_ascii=False, indent=4)
