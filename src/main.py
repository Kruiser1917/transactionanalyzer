import argparse

import pandas as pd

from reports import expenses_by_category, expenses_by_day_of_week, expenses_by_workday_weekend
from services import (
    analyze_cashback,
    analyze_investment,
    individual_transfers_search,
    phone_number_search,
    simple_search,
)
from views import events_page, main_page


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load transaction data from an Excel file.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        pd.DataFrame: The loaded transaction data.
    """
    return pd.read_excel(file_path)


def main():
    """
    Main function to execute actions based on provided arguments.
    """
    parser = argparse.ArgumentParser(description="Transaction Analyzer")
    parser.add_argument('--file', required=True, help='Path to the Excel file with transactions.')
    parser.add_argument(
        '--action', required=True,
        choices=[
            'main_page', 'events_page', 'expenses_by_category',
            'expenses_by_day_of_week', 'expenses_by_workday_weekend',
            'analyze_cashback', 'analyze_investment', 'simple_search',
            'phone_number_search', 'individual_transfers_search'
        ],
        help='Action to perform.'
    )
    parser.add_argument('--year', type=int, help='Year for the analysis.')
    parser.add_argument('--month', type=int, help='Month for the analysis.')
    parser.add_argument('--query', type=str, help='Query string for searching transactions.')
    parser.add_argument('--phone', type=str, help='Phone number for searching transactions.')
    parser.add_argument('--name', type=str, help='Individual name for searching transactions.')

    args = parser.parse_args()

    data = load_data(args.file)

    if args.action == 'main_page':
        current_time_str = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        result = main_page(data, current_time_str)
    elif args.action == 'events_page':
        current_time_str = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        result = events_page(data, current_time_str)
    elif args.action == 'expenses_by_category':
        if not args.year or not args.month:
            raise ValueError("Year and month must be provided for expenses_by_category action.")
        result = expenses_by_category(data, args.year, args.month)
    elif args.action == 'expenses_by_day_of_week':
        if not args.year or not args.month:
            raise ValueError("Year and month must be provided for expenses_by_day_of_week action.")
        result = expenses_by_day_of_week(data, args.year, args.month)
    elif args.action == 'expenses_by_workday_weekend':
        if not args.year or not args.month:
            raise ValueError("Year and month must be provided for expenses_by_workday_weekend action.")
        result = expenses_by_workday_weekend(data, args.year, args.month)
    elif args.action == 'analyze_cashback':
        if not args.year or not args.month:
            raise ValueError("Year and month must be provided for analyze_cashback action.")
        result = analyze_cashback(data, args.year, args.month)
    elif args.action == 'analyze_investment':
        if not args.year or not args.month:
            raise ValueError("Year and month must be provided for analyze_investment action.")
        result = analyze_investment(data, args.year, args.month)
    elif args.action == 'simple_search':
        if not args.query:
            raise ValueError("Query must be provided for simple_search action.")
        result = simple_search(data, args.query)
    elif args.action == 'phone_number_search':
        if not args.phone:
            raise ValueError("Phone number must be provided for phone_number_search action.")
        result = phone_number_search(data, args.phone)
    elif args.action == 'individual_transfers_search':
        if not args.name:
            raise ValueError("Individual name must be provided for individual_transfers_search action.")
        result = individual_transfers_search(data, args.name)
    else:
        raise ValueError("Unknown action provided.")

    print(result)


if __name__ == "__main__":
    main()
