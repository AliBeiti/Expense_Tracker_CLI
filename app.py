"""Expence tracker Application"""
import argparse
import os
from datetime import datetime
import time
import json
import csv

EXPENSES_FILE = "expenses.json"
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def positive_float(value):
    """this function handles errors for nonpositive amount inputs"""
    try:
        f = float(value)
        if f <= 0:
            raise argparse.ArgumentTypeError(
                "Amount must be a positive number.")
        return f
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Amount must be a number.") from exc


def argument_parser():
    """This function handles CLI inputs"""
    parser = argparse.ArgumentParser(description="Expense Tracker App")
    subparser = parser.add_subparsers(dest="command")

    # Add expense
    add = subparser.add_parser("add", help="add a new expense")
    add.add_argument("description", type=str,
                     help="Description of the Expense.")
    add.add_argument("amount",
                     type=positive_float, help="amount of the expense")
    add.add_argument("--category", type=str,
                     help="category of the expense", default="other")

    # Delete expense
    delete = subparser.add_parser(
        "delete", help="delete an expense using its ID")
    delete.add_argument("id", type=int,
                        help="id of the expense")

    # Update expense
    update = subparser.add_parser(
        "update", help="update existing expense using its id")
    update.add_argument("id", type=int,
                        help="id of the expense")
    update.add_argument("--description", type=str, default='',
                        help="new description for the expense")
    update.add_argument("--amount", default=0, type=positive_float,
                        help="new amount for the expense")
    update.add_argument("--category", type=str, default='',
                        help="new category for the expense")

    # list expenses
    show_list = subparser.add_parser(
        "list", help="list expenses(optionally sorted)")
    show_list.add_argument("--category", type=str, default='',
                           help="list expenses using their category")
    show_list.add_argument("--month", type=int, choices=range(1, 13), default=0,
                           help="list expenses based on the month")
    # summary
    summary = subparser.add_parser(
        "summary", help="give a summary of the expenses(optionally sorted)")
    summary.add_argument("--category", type=str, default='',
                         help="summary expenses using their category")
    summary.add_argument("--month", type=int, choices=range(1, 13), default=0,
                         help="summary expenses based on the month")

    # export
    export = subparser.add_parser(
        "export", help="export a csv file of the expenses(optionally sorted)")
    export.add_argument("--filename", type=str,
                        default="expenses.csv", help="expenses filename")
    export.add_argument("--category", type=str, default='',
                        help="export expenses using their category")
    export.add_argument("--month", type=int, choices=range(1, 13), default=0,
                        help="export expenses based on the month")

    return parser


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
    """This function adds new expenses to list"""
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


def delete_expense(expense_id):
    """Deletes an expense from the files using the ID"""
    expenses = load_expenses()
    expense_found = False
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            del expenses[index]
            expense_found = True
            print(
                f"Expesne deleted: {expense['description']} (ID:{expense['id']}) (Amount:{expense["amount"]}) ")
            break
    expense_search(expense_found, expense_id)
    save_expenses(expenses=expenses)


def update_expense(expense_id, new_description, new_amount, new_category):
    """Updates a task with the ID"""
    expenses = load_expenses()
    expense_found = False
    for expense in expenses:
        if expense["id"] == expense_id:
            if new_description != '':
                expense["description"] = new_description
            if new_amount != 0:
                expense["amount"] = new_amount
            if new_category != '':
                expense["category"] = new_category
            expense["updatedAt"] = time.time()
            expense_found = True
            print(
                f"Expense updated: {expense['description']} (ID:{expense['id']}) (Amount:{expense["amount"]}) (Category: {expense["category"]}) ")
            break
    expense_search(expense_found, expense_id)
    save_expenses(expenses=expenses)


def sort_expenses(month, category):
    """sort the expenses based on month or category or both"""
    expenses = load_expenses()
    sorted_expenses = []
    for expense in expenses:
        dt = datetime.fromtimestamp(expense["createdAt"])

        matches_month = (month == 0 or dt.month == month)
        matches_category = (category == '' or expense["category"] == category)

        if matches_month and matches_category:
            sorted_expenses.append(expense)

    return sorted_expenses


def summary_expenses(month, category):
    """give a summary of expenses based on category or mmonth"""

    expenses = sort_expenses(month, category)
    total = sum(expense["amount"] for expense in expenses)

    if month and category:
        print(f"Total Expenses for {category} in {MONTHS[month-1]}: {total}$")
    elif month:
        print(f"Total Expenses {MONTHS[month-1]}: {total}$")
    elif category:
        print(f"Total Expenses for {category}: {total}$")
    else:
        print(f"Total Expenses: {total}$")


def list_expenses(month, category):
    """list and show the expenses (optonally can be sorted by month or category)"""

    expenes = sort_expenses(month, category)

    if month and category:
        print(f"Expense list for {category} in {MONTHS[month-1]}:")
    elif month:
        print(f"Expense list in {MONTHS[month-1]}:")
    elif category:
        print(f"Expense list for {category}:")
    else:
        print("Total Expense list:")

    print("*" * 40)

    print(f"{'ID':<5} {'Description':<65} {'amount':<9} {'category':<25} {'Created At':<20}")
    print("-" * 130)

    for expense in expenes:
        dt = datetime.fromtimestamp(expense["createdAt"])
        print(
            f"{expense["id"]:<5} {expense["description"]:<65} ${expense["amount"]:<8} {expense["category"]:<25} {dt}")


def export_expenses(filename, month, category):
    """This function exports expenses into a csv file"""
    if filename[-4:] != ".csv":
        filename += ".csv"
    headers = ["Id", "Description", "Amount",
               "Category", "Created At", "Updatet At"]
    expenses = sort_expenses(month, category)

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(headers)

        for expense in expenses:
            dt_create = datetime.fromtimestamp(
                expense["createdAt"]).strftime("%Y-%m-%d %H:%M:%S")
            dt_update = datetime.fromtimestamp(
                expense["updatedAt"]).strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([expense["id"], expense["description"],
                            expense["amount"], expense["category"], dt_create, dt_update])


def main():
    "Main function"
    args = argument_parser().parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount, args.category)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount, args.category)
    elif args.command == "summary":
        summary_expenses(args.month, args.category)
    elif args.command == "list":
        list_expenses(args.month, args.category)
    elif args.command == "export":
        export_expenses(args.filename, args.month, args.category)
    else:
        argument_parser().print_help()


if __name__ == "__main__":
    main()
