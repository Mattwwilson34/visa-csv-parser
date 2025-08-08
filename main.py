#!/usr/bin/env python

import csv
import sys
from collections import Counter
from datetime import datetime, timedelta

from tabulate import tabulate

CSV_PATH = "./raw_data/master_chase_visa_activity_2023_08_04_2025_08_04.CSV"

# Field name constants
TRANSACTION_DATE = "Transaction Date"
POST_DATE = "Post Date"
DESCRIPTION = "Description"
CATEGORY = "Category"
TYPE = "Type"
AMOUNT = "Amount"
MEMO = "Memo"

# Required fields set
REQUIRED_FIELDS = {TRANSACTION_DATE, POST_DATE, DESCRIPTION, CATEGORY, TYPE, AMOUNT, MEMO}


def validate_csv_headers(fieldnames):
    """Validate that CSV has all required fields."""
    missing_fields = REQUIRED_FIELDS - set(fieldnames)
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")


def parse_date(date_str):
    """Parse dates like '8/2/23' or '12/25/23'."""
    return datetime.strptime(date_str, "%m/%d/%y")  # Note: %y for 2-digit year


def main():

    with open(CSV_PATH, "r") as file:
        transactions = csv.DictReader(file)
        validate_csv_headers(transactions.fieldnames)

        twelve_months_ago = datetime.now() - timedelta(days=365)

        desc_amount_counts = Counter(
            (row[DESCRIPTION], row[AMOUNT])
            for row in transactions
            if parse_date(row[TRANSACTION_DATE]) >= twelve_months_ago
        )

        table_data = [
            [desc, f"${amount}", count, f"${float(amount) * count:.2f}"]
            for (desc, amount), count in desc_amount_counts.most_common(50)
        ]

        headers = ["Description", "Amount", "Frequency", "Total Spent"]

        print("LAST 12 MONTHS")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    sys.exit(main())
