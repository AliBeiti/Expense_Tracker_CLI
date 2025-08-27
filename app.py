import argparse
import os
from datetime import datetime
import time
import json

EXPENSES_FILE = "expenses.json"


def argument_parser():
    parser = argparse.ArgumentParser(description="Expense Tracker App")
    subparser = parser.add_subparsers(dest="command")

    # Add expense
    add = subparser.add_parser("add", help="add a new expense")
    add.add_argument("description", type=str,
                     help="Description of the Expense.")
    add.add_argument("amount", type=float, help="amount of the expense")
    add.add_argument("category", type=str,
                     help="category of the expense", default="other")

    # Delete expense
    delete = subparser.add_parser(
        "delete", help="delete an expense using its ID")
    delete.add_argument("id", type=int, help="id of the expense")

    # Update expense
    update = subparser.add_parser(
        "update", help="update existing expense using its id")
    update.add_argument("id", type=int, help="id of the expense")
    update.add_argument("--description", type=str, default='',
                        help="new description for the expense")
    update.add_argument("--amount", type=int, default=0,
                        help="new amount for the expense")
    update.add_argument("--category", type=str, default='',
                        help="new category for the expense")

    # list expenses
    show_list = subparser.add_parser(
        "list", help="list expenses(optionally sorted)")
    show_list.add_argument("--category", type=str,
                           help="list expenses using their category")
    show_list.add_argument("--month", type=int, choices=range(1, 13),
                           help="list expenses based on the month")
    # summary
    summary = subparser.add_parser(
        "summary", help="give a summary of the expenses(optionally sorted)")
    summary.add_argument("--category", type=str,
                         help="summary expenses using their category")
    summary.add_argument("--month", type=int, choices=range(1, 13),
                         help="summary expenses based on the month")

    # export
    export = subparser.add_parser(
        "export", help="export a csv file of the expenses(optionally sorted)")
    export.add_argument("--filename", type=str,
                        default="expenses.csv", help="expenses filename")
    export.add_argument("--category", type=str,
                        help="export expenses using their category")
    export.add_argument("--month", type=int, choices=range(1, 13),
                        help="export expenses based on the month")

    return parser.parse_args()


def load_expenses():
    """initilizing file. creates one if it does not exist."""
    if os.path.exists(EXPENSES_FILE):
        try:
            with open(EXPENSES_FILE, "r", encoding="utf-8") as file:
                expenses = json.load(file)
                return expenses
        except json.JSONDecodeError:
            print("Warning: Could not decode expenses.json. Starting fresh.")
    return []


def save_expenses(expenses):
    """Saves list of expenses into the database file."""
    with open(EXPENSES_FILE, 'w', encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def expense_search(expense_found, expense_id):
    """This function prints error message if there is no expense with the ID in Database."""
    if expense_found is False:
        print(f"Expense with ID:{expense_id} not found.")


def add_expense(description, amount, category):
    expenses = load_expenses()
    if len(expenses) > 0:
        next_id = max([expense["id"] for expense in expenses]) + 1
    else:
        next_id = 1
    expense = {"id": next_id, "description": description, "amount": amount,
               "category": category, "createdAt": time.time(), "updatedAt": time.time()}
    expenses.append(expense)
    print(f"Expense added successfully (ID:{next_id})")
    save_expenses(expenses=expenses)
