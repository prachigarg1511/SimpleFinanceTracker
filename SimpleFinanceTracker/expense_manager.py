"""
expense_manager.py
------------------
Handles all expense CRUD operations.
"""

import csv
from datetime import datetime
from helpers import EXPENSE_FILE


class ExpenseManager:

    def __init__(self):
        self.file = EXPENSE_FILE

    # -------------------------------
    # Read all expenses
    # -------------------------------
    COLUMNS = ["Date", "Expense", "Category", "Amount", "Payment", "Notes"]

    def get_all_expenses(self):

        expenses = []

        try:
            with open(self.file, "r", newline="", encoding="utf-8") as file:

                reader = csv.DictReader(file)

                # If the header row is missing/corrupt, fieldnames won't match
                if reader.fieldnames != self.COLUMNS:
                    return []

                for row in reader:
                    try:
                        row["Amount"] = float(row["Amount"])
                        expenses.append(row)
                    except (ValueError, TypeError):
                        pass  # skip bad rows

        except FileNotFoundError:
            pass

        return expenses

    # -------------------------------
    # Add Expense
    # -------------------------------
    def add_expense(
            self,
            date,
            expense,
            category,
            amount,
            payment,
            notes):

        with open(self.file, "a", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                date,
                expense,
                category,
                amount,
                payment,
                notes
            ])

    # -------------------------------
    # Delete Expense
    # -------------------------------
    def delete_expense(self, index):

        expenses = self.get_all_expenses()

        if index < len(expenses):

            expenses.pop(index)

        self.save_all(expenses)

    # -------------------------------
    # Update Expense
    # -------------------------------
    def update_expense(self, index, updated):

        expenses = self.get_all_expenses()

        if index < len(expenses):

            expenses[index] = updated

        self.save_all(expenses)

    # -------------------------------
    # Save all expenses
    # -------------------------------
    def save_all(self, expenses):

        with open(self.file, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Date",
                "Expense",
                "Category",
                "Amount",
                "Payment",
                "Notes"
            ])

            for expense in expenses:

                writer.writerow([
                    expense["Date"],
                    expense["Expense"],
                    expense["Category"],
                    expense["Amount"],
                    expense["Payment"],
                    expense["Notes"]
                ])

    # -------------------------------
    # Search Expense
    # -------------------------------
    def search(self, keyword):

        keyword = keyword.lower()

        result = []

        for expense in self.get_all_expenses():

            if (
                keyword in expense["Expense"].lower()
                or keyword in expense["Category"].lower()
                or keyword in expense["Payment"].lower()
                or keyword in expense["Notes"].lower()
            ):

                result.append(expense)

        return result

    # -------------------------------
    # Filter Category
    # -------------------------------
    def filter_category(self, category):

        return [

            expense

            for expense in self.get_all_expenses()

            if expense["Category"] == category

        ]

    # -------------------------------
    # Today's Expenses
    # -------------------------------
    def today_total(self):

        today = datetime.now().strftime("%d-%m-%Y")

        total = 0

        for expense in self.get_all_expenses():

            if expense["Date"] == today:

                total += expense["Amount"]

        return total

    # -------------------------------
    # Monthly Total
    # -------------------------------
    def monthly_total(self):

        month = datetime.now().strftime("%m-%Y")

        total = 0

        for expense in self.get_all_expenses():

            if expense["Date"][3:] == month:

                total += expense["Amount"]

        return total

    # -------------------------------
    # Highest Expense
    # -------------------------------
    def highest_expense(self):

        expenses = self.get_all_expenses()

        if not expenses:

            return None

        return max(expenses, key=lambda x: x["Amount"])

    # -------------------------------
    # Category Summary
    # -------------------------------
    def category_summary(self):

        summary = {}

        for expense in self.get_all_expenses():

            category = expense["Category"]

            summary[category] = summary.get(category, 0)

            summary[category] += expense["Amount"]

        return summary

    # -------------------------------
    # Total Expenses
    # -------------------------------
    def total_expense(self):

        total = 0

        for expense in self.get_all_expenses():

            total += expense["Amount"]

        return total

    # -------------------------------
    # Total Records
    # -------------------------------
    def total_records(self):

        return len(self.get_all_expenses())