"""
add_expense.py
-----------------------
Add Expense Window
"""

import tkinter as tk
from tkinter import ttk, messagebox

from helpers import (
    today,
    get_theme,
    NORMAL_FONT
)

from expense_manager import ExpenseManager


class AddExpenseWindow:

    def __init__(self, parent, refresh_callback):

        self.manager = ExpenseManager()

        self.refresh_callback = refresh_callback

        self.theme = get_theme()

        self.window = tk.Toplevel(parent)

        self.window.title("Add Expense")

        self.window.geometry("500x520")

        self.window.resizable(False, False)

        self.window.configure(bg=self.theme["bg"])

        self.create_widgets()

    # -----------------------------------------

    def create_widgets(self):

        title = tk.Label(

            self.window,

            text="Add New Expense",

            font=("Segoe UI", 18, "bold"),

            bg=self.theme["bg"]

        )

        title.pack(pady=20)

        frame = tk.Frame(

            self.window,

            bg=self.theme["bg"]

        )

        frame.pack(padx=30)

        # Date

        tk.Label(
            frame,
            text="Date",
            font=NORMAL_FONT,
            bg=self.theme["bg"]
        ).grid(row=0, column=0, sticky="w", pady=8)

        self.date = ttk.Entry(frame, width=30)

        self.date.insert(0, today())

        self.date.grid(row=0, column=1)

        # Expense Name

        tk.Label(
            frame,
            text="Expense Name",
            font=NORMAL_FONT,
            bg=self.theme["bg"]
        ).grid(row=1, column=0, sticky="w", pady=8)

        self.expense = ttk.Entry(frame, width=30)

        self.expense.grid(row=1, column=1)

        # Category

        tk.Label(
            frame,
            text="Category",
            font=NORMAL_FONT,
            bg=self.theme["bg"]
        ).grid(row=2, column=0, sticky="w", pady=8)

        self.category = ttk.Combobox(

            frame,

            values=[
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Medical",
                "Education",
                "Entertainment",
                "Office",
                "Others"
            ],

            width=27

        )

        self.category.current(0)

        self.category.grid(row=2, column=1)

        # Amount

        tk.Label(
            frame,
            text="Amount",
            font=NORMAL_FONT,
            bg=self.theme["bg"]
        ).grid(row=3, column=0, sticky="w", pady=8)

        self.amount = ttk.Entry(frame, width=30)

        self.amount.grid(row=3, column=1)

        # Payment

        tk.Label(
            frame,
            text="Payment",
            font=NORMAL_FONT,
            bg=self.theme["bg"]
        ).grid(row=4, column=0, sticky="w", pady=8)

        self.payment = ttk.Combobox(

            frame,

            values=[
                "Cash",
                "UPI",
                "Card",
                "Net Banking"
            ],

            width=27

        )

        self.payment.current(0)

        self.payment.grid(row=4, column=1)

        # Notes

        tk.Label(
            frame,
            text="Notes",
            font=NORMAL_FONT,
            bg=self.theme["bg"]
        ).grid(row=5, column=0, sticky="nw", pady=8)

        self.notes = tk.Text(

            frame,

            width=28,

            height=5

        )

        self.notes.grid(row=5, column=1)

        ttk.Button(

            self.window,

            text="Save Expense",

            command=self.save

        ).pack(pady=20)

    # -----------------------------------------

    def save(self):

        expense = self.expense.get().strip()

        category = self.category.get()

        amount = self.amount.get().strip()

        payment = self.payment.get()

        notes = self.notes.get("1.0", "end").strip()

        date = self.date.get().strip()

        if expense == "":

            messagebox.showerror(
                "Error",
                "Expense Name Required"
            )

            return

        try:

            amount = float(amount)

        except:

            messagebox.showerror(
                "Error",
                "Amount should be numeric"
            )

            return

        self.manager.add_expense(

            date,

            expense,

            category,

            amount,

            payment,

            notes

        )

        messagebox.showinfo(

            "Success",

            "Expense Added Successfully."

        )

        self.refresh_callback()

        self.window.destroy()