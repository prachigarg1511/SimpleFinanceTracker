"""
analytics.py
Expense Analytics Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from collections import defaultdict

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class AnalyticsWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Expense Analytics")
        self.window.geometry("1200x700")
        self.window.configure(bg="#F4F6F8")

        self.file = "database/expenses.csv"

        self.category_data = defaultdict(float)

        self.load_data()

        self.create_ui()

    # ------------------------------

    def load_data(self):

        self.category_data.clear()

        if not os.path.exists(self.file):
            return

        with open(self.file, newline="", encoding="utf-8") as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                try:

                    category = row["Category"]

                    amount = float(row["Amount"])

                    self.category_data[category] += amount

                except:

                    pass

    # ------------------------------

    def create_ui(self):

        title = tk.Label(

            self.window,

            text="Expense Analytics Dashboard",

            font=("Segoe UI",22,"bold"),

            bg="#F4F6F8"

        )

        title.pack(pady=15)

        self.main = tk.Frame(
            self.window,
            bg="#F4F6F8"
        )

        self.main.pack(fill="both", expand=True)

        self.left = tk.Frame(
            self.main,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.right = tk.Frame(
            self.main,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.draw_pie_chart()
    
        # ------------------------------

    def draw_pie_chart(self):

        if len(self.category_data)==0:

            tk.Label(

                self.left,

                text="No Expense Data",

                font=("Segoe UI",16),

                bg="white"

            ).pack(pady=100)

            return

        fig = Figure(figsize=(5,5), dpi=100)

        ax = fig.add_subplot(111)

        labels = list(self.category_data.keys())

        values = list(self.category_data.values())

        ax.pie(

            values,

            labels=labels,

            autopct="%1.1f%%",

            startangle=90

        )

        ax.set_title("Expense by Category")

        canvas = FigureCanvasTkAgg(fig, master=self.left)

        canvas.draw()

        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.draw_bar_chart()

        # ------------------------------

    def draw_bar_chart(self):

        fig = Figure(figsize=(5,5), dpi=100)

        ax = fig.add_subplot(111)

        categories = list(self.category_data.keys())
        amounts = list(self.category_data.values())

        ax.bar(categories, amounts)

        ax.set_title("Expense by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount (₹)")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.right)

        canvas.draw()

        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.create_summary()

    # ------------------------------

    def create_summary(self):

        summary = tk.Frame(
            self.window,
            bg="#F4F6F8"
        )

        summary.pack(fill="x", padx=20, pady=10)

        total = sum(self.category_data.values())

        if len(self.category_data) > 0:

            highest = max(
                self.category_data,
                key=self.category_data.get
            )

            highest_amount = self.category_data[highest]

            average = total / len(self.category_data)

        else:

            highest = "N/A"
            highest_amount = 0
            average = 0

        self.create_card(
            summary,
            "Total Expense",
            f"₹ {total:.2f}"
        )

        self.create_card(
            summary,
            "Highest Category",
            f"{highest}\n₹ {highest_amount:.2f}"
        )

        self.create_card(
            summary,
            "Average",
            f"₹ {average:.2f}"
        )

        tk.Button(
            summary,
            text="Refresh",
            bg="#2563EB",
            fg="white",
            font=("Segoe UI",10,"bold"),
            command=self.refresh
        ).pack(side="right", padx=10)

        tk.Button(
            summary,
            text="Close",
            bg="#EF4444",
            fg="white",
            font=("Segoe UI",10,"bold"),
            command=self.window.destroy
        ).pack(side="right")

    # ------------------------------

    def create_card(self, parent, title, value):

        frame = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            width=220,
            height=90
        )

        frame.pack(
            side="left",
            padx=10
        )

        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI",11),
            bg="white"
        ).pack(pady=(10,0))

        tk.Label(
            frame,
            text=value,
            font=("Segoe UI",15,"bold"),
            bg="white"
        ).pack()

    # ------------------------------

    def refresh(self):

        self.left.destroy()
        self.right.destroy()

        self.load_data()

        self.left = tk.Frame(
            self.main,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.right = tk.Frame(
            self.main,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.draw_pie_chart()