# 🧾 Expense Tracker CLI

A simple and user-friendly command-line tool to track your expenses using Python. A project from https://roadmap.sh/projects/expense-tracker.

## 🚀 Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/AliBeiti/Expense_Tracker_CLI.git
```

## Requirements

Python 3.7+

## Usage

```bash
expense-tracker add "Buy Milk" 2.5 --category "groceries"
expense-tracker list --month 8 --categort "groceries"
expense-tracker delete 1
expense-tracker update 2 --amount 4.99
expense-tracker summary --category "groceries"
expense-tracker export --filename "AugustReport.csv"
```
