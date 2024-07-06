import sys
import os
import pandas as pd
import argparse
from datetime import datetime
from views import main_page, events_page
from reports import (
    expenses_by_category,
    expenses_by_day_of_week,
    expenses_by_workday_weekend,
    expenses_by_hour,
)
from services import (
    analyze_cashback_categories,
    analyze_investment,
    simple_search,
    phone_number_search,
    individual_transfers_search,
)

# Добавление пути к модулю src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def load_data(file_path):
    # Загрузка данных из файла Excel
    data = pd.read_excel(file_path)
    return data


def main():
    """
    Main function to handle different actions for transaction analysis.

    Parses command line arguments and executes the corresponding action.

    Args:
        None

    Returns:
        None
    """
    # ваш код


def main():
    parser = argparse.ArgumentParser(description="Transaction Analysis Tool")
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the Excel file with transactions",
    )
    parser.add_argument(
        "--action",
        type=str,
        required=True,
        choices=[
            "main_page",
            "events_page",
            "expenses_by_category",
            "expenses_by_day_of_week",
            "expenses_by_workday_weekend",
            "expenses_by_hour",
            "analyze_cashback",
            "analyze_investment",
            "simple_search",
            "phone_number_search",
            "individual_transfers_search",
        ],
        help="Action to perform",
    )
    parser.add_argument("--year", type=int, help="Year for the report")
    parser.add_argument("--month", type=int, help="Month for the report")
    parser.add_argument("--query", type=str, help="Query for search actions")
    parser.add_argument("--phone", type=str, help="Phone number for search actions")
    parser.add_argument("--name", type=str, help="Individual name for search actions")
    args = parser.parse_args()

    data = load_data(args.file)

    if args.action == "main_page":
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = main_page()
    elif args.action == "events_page":
        current_time_str = datetime.now().strftime("%Y-%m-%d")
        result = events_page(current_time_str, period="M")
    elif args.action == "expenses_by_category":
        result = expenses_by_category()
    elif args.action == "expenses_by_day_of_week":
        result = expenses_by_day_of_week(args.year, args.month)
    elif args.action == "expenses_by_workday_weekend":
        result = expenses_by_workday_weekend(data, args.year, args.month)
    elif args.action == "expenses_by_hour":
        result = expenses_by_hour(data, args.year, args.month)
    elif args.action == "analyze_cashback":
        result = analyze_cashback_categories(data, args.year, args.month)
    elif args.action == "analyze_investment":
        result = analyze_investment(data, args.year, args.month)
    elif args.action == "simple_search":
        result = simple_search(data, args.query)
    elif args.action == "phone_number_search":
        result = phone_number_search(data, args.phone)
    elif args.action == "individual_transfers_search":
        result = individual_transfers_search(data, args.name)

    print(result)


if __name__ == "__main__":
    main()
