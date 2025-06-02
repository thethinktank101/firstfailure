import json
import os

DATA_FILE = "expenses.json"

def load_data():
    if not os.path.isfile(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_data(expenses):
    with open(DATA_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses, expense):
    expenses.append(expense)

def get_summary(expenses):
    total = sum(e['amount'] for e in expenses)
    category_totals = {}
    for e in expenses:
        category_totals[e['category']] = category_totals.get(e['category'], 0) + e['amount']
    return total, category_totals
