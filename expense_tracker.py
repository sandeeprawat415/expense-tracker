"""
Expense Tracker
===============
A simple command-line expense tracker that stores data locally in a
JSON file. Supports adding, viewing, filtering, summarizing, and
exporting expenses to CSV.

Author: Sandy
"""

from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Optional


DATA_FILE = "expenses.json"
DATE_FORMAT = "%Y-%m-%d"


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------

@dataclass
class Expense:
    id: int
    date: str          # stored as "YYYY-MM-DD"
    category: str
    amount: float
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Expense":
        return Expense(
            id=data["id"],
            date=data["date"],
            category=data["category"],
            amount=data["amount"],
            note=data.get("note", ""),
        )


# --------------------------------------------------------------------------
# Storage + business logic
# --------------------------------------------------------------------------

class ExpenseTracker:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.expenses: List[Expense] = []
        self._load()

    # ---- persistence ----------------------------------------------------

    def _load(self) -> None:
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                try:
                    raw = json.load(f)
                except json.JSONDecodeError:
                    raw = []
            self.expenses = [Expense.from_dict(e) for e in raw]
        else:
            self.expenses = []

    def _save(self) -> None:
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.expenses], f, indent=2)

    # ---- core operations --------------------------------------------------

    def add_expense(self, date: str, category: str, amount: float, note: str = "") -> Expense:
        new_id = (max((e.id for e in self.expenses), default=0)) + 1
        expense = Expense(id=new_id, date=date, category=category.strip().title(),
                           amount=round(amount, 2), note=note.strip())
        self.expenses.append(expense)
        self._save()
        return expense

    def delete_expense(self, expense_id: int) -> bool:
        before = len(self.expenses)
        self.expenses = [e for e in self.expenses if e.id != expense_id]
        changed = len(self.expenses) != before
        if changed:
            self._save()
        return changed

    def list_expenses(self, category: Optional[str] = None,
                       month: Optional[str] = None) -> List[Expense]:
        """month should be in 'YYYY-MM' format if provided."""
        results = self.expenses
        if category:
            results = [e for e in results if e.category.lower() == category.lower()]
        if month:
            results = [e for e in results if e.date.startswith(month)]
        return sorted(results, key=lambda e: e.date)

    def total(self, category: Optional[str] = None, month: Optional[str] = None) -> float:
        return round(sum(e.amount for e in self.list_expenses(category, month)), 2)

    def category_summary(self, month: Optional[str] = None) -> dict:
        summary: dict = {}
        for e in self.list_expenses(month=month):
            summary[e.category] = round(summary.get(e.category, 0) + e.amount, 2)
        return dict(sorted(summary.items(), key=lambda kv: kv[1], reverse=True))

    def monthly_summary(self) -> dict:
        summary: dict = {}
        for e in self.expenses:
            month = e.date[:7]  # YYYY-MM
            summary[month] = round(summary.get(month, 0) + e.amount, 2)
        return dict(sorted(summary.items()))

    def export_csv(self, filepath: str = "expenses_export.csv") -> str:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Category", "Amount", "Note"])
            for e in sorted(self.expenses, key=lambda e: e.date):
                writer.writerow([e.id, e.date, e.category, e.amount, e.note])
        return filepath


# --------------------------------------------------------------------------
# CLI helpers
# --------------------------------------------------------------------------

def prompt_date(default_today: bool = True) -> str:
    raw = input(f"Date (YYYY-MM-DD) [Enter = today]: ").strip()
    if not raw and default_today:
        return datetime.today().strftime(DATE_FORMAT)
    try:
        datetime.strptime(raw, DATE_FORMAT)
        return raw
    except ValueError:
        print("Invalid date format, using today's date instead.")
        return datetime.today().strftime(DATE_FORMAT)


def prompt_amount() -> float:
    while True:
        raw = input("Amount: ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("Amount must be positive.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number.")


def print_expenses(expenses: List[Expense]) -> None:
    if not expenses:
        print("No expenses found.\n")
        return
    print(f"\n{'ID':<4}{'Date':<12}{'Category':<15}{'Amount':<10}Note")
    print("-" * 60)
    for e in expenses:
        print(f"{e.id:<4}{e.date:<12}{e.category:<15}{e.amount:<10}{e.note}")
    print()


def print_summary(summary: dict, label: str = "Category") -> None:
    if not summary:
        print("No data to summarize.\n")
        return
    print(f"\n{label:<15}Amount")
    print("-" * 30)
    for key, amount in summary.items():
        print(f"{key:<15}{amount}")
    print()


# --------------------------------------------------------------------------
# Menu / main loop
# --------------------------------------------------------------------------

MENU = """
========== EXPENSE TRACKER ==========
1. Add expense
2. View all expenses
3. View expenses by category
4. View expenses by month
5. Category-wise summary
6. Monthly summary
7. Delete expense
8. Export to CSV
9. Exit
======================================
"""


def main() -> None:
    tracker = ExpenseTracker()

    while True:
        print(MENU)
        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            date = prompt_date()
            category = input("Category (e.g. Food, Travel, Rent): ").strip() or "Other"
            amount = prompt_amount()
            note = input("Note (optional): ").strip()
            expense = tracker.add_expense(date, category, amount, note)
            print(f"Added expense #{expense.id}: {expense.category} - ₹{expense.amount}\n")

        elif choice == "2":
            print_expenses(tracker.list_expenses())

        elif choice == "3":
            category = input("Enter category: ").strip()
            expenses = tracker.list_expenses(category=category)
            print_expenses(expenses)
            print(f"Total in '{category}': ₹{tracker.total(category=category)}\n")

        elif choice == "4":
            month = input("Enter month (YYYY-MM): ").strip()
            expenses = tracker.list_expenses(month=month)
            print_expenses(expenses)
            print(f"Total for {month}: ₹{tracker.total(month=month)}\n")

        elif choice == "5":
            month = input("Filter by month (YYYY-MM) [Enter = all time]: ").strip() or None
            print_summary(tracker.category_summary(month=month), label="Category")

        elif choice == "6":
            print_summary(tracker.monthly_summary(), label="Month")

        elif choice == "7":
            try:
                expense_id = int(input("Enter expense ID to delete: ").strip())
            except ValueError:
                print("Invalid ID.\n")
                continue
            if tracker.delete_expense(expense_id):
                print(f"Deleted expense #{expense_id}.\n")
            else:
                print(f"No expense found with ID {expense_id}.\n")

        elif choice == "8":
            path = tracker.export_csv()
            print(f"Exported to {path}\n")

        elif choice == "9":
            print("Goodbye! Keep those finances in check.")
            break

        else:
            print("Invalid option, please choose 1-9.\n")


if __name__ == "__main__":
    main()
