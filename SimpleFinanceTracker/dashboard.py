"""
dashboard.py
Professional Dashboard
"""

import tkinter as tk
from tkinter import ttk, messagebox

from helpers import (
    get_theme,
    TITLE_FONT,
    NORMAL_FONT,
    money
)

from expense_manager import ExpenseManager


class Dashboard:

    def __init__(self, username):

        self.username = username
        self.theme = get_theme()
        self.manager = ExpenseManager()

        self.root = tk.Tk()
        self.root.title("Simple Finance Tracker")
        self.root.geometry("1400x800")
        self.root.configure(bg=self.theme["bg"])

        self.create_ui()
        self.refresh_dashboard()

        self.root.mainloop()

    # ----------------------------------------------------

    def create_ui(self):

        self.create_sidebar()

        self.main = tk.Frame(
            self.root,
            bg=self.theme["bg"]
        )

        self.main.pack(side="left", fill="both", expand=True)

        self.create_header()

        self.create_cards()

        self.create_search()

        self.create_table()

        self.create_bottom_buttons()

        self.create_status()

    # ----------------------------------------------------

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            width=220,
            bg=self.theme["primary"]
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        logo = tk.Label(

            self.sidebar,

            text="💰\nFinance\nTracker",

            bg=self.theme["primary"],

            fg="white",

            font=("Segoe UI", 20, "bold")

        )

        logo.pack(pady=25)

        self.sidebar_button(
            "🏠 Dashboard",
            self.refresh_dashboard
        )

        self.sidebar_button(
            "➕ Add Expense",
            self.open_add_expense
        )

        self.sidebar_button(
            "📊 Analytics",
            self.open_analytics
        )

        self.sidebar_button(
            "💰 Budget",
            self.open_budget
        )

        self.sidebar_button(
            "📄 Reports",
            self.open_reports
        )

        self.sidebar_button(
            "⚙ Settings",
            self.open_settings
        )

        tk.Button(

            self.sidebar,

            text="🚪 Logout",

            bg="#e74c3c",

            fg="white",

            relief="flat",

            command=self.logout

        ).pack(

            side="bottom",

            fill="x",

            padx=15,

            pady=20

        )

    # ----------------------------------------------------

    def open_analytics(self):

        from analytics import AnalyticsWindow
        AnalyticsWindow(self.root)

    # ----------------------------------------------------

    def open_budget(self):

        from budget import BudgetWindow
        BudgetWindow(self.root)

    # ----------------------------------------------------

    def open_reports(self):

        from reports import ReportsWindow
        ReportsWindow(self.root)

    # ----------------------------------------------------

    def open_settings(self):

        from settings import SettingsWindow
        SettingsWindow(self.root, self.username)



    def sidebar_button(self, text, command):

        tk.Button(

            self.sidebar,

            text=text,

            command=command,

            bg=self.theme["primary"],

            fg="white",

            relief="flat",

            font=("Segoe UI", 11),

            activebackground=self.theme["secondary"],

            activeforeground="white"

        ).pack(

            fill="x",

            padx=10,

            pady=4

        )

    # ----------------------------------------------------

    def create_header(self):

        tk.Label(

            self.main,

            text=f"Welcome, {self.username}",

            font=TITLE_FONT,

            bg=self.theme["bg"]

        ).pack(

            anchor="w",

            padx=20,

            pady=15

        )

    # ----------------------------------------------------

    def create_cards(self):

        frame = tk.Frame(

            self.main,

            bg=self.theme["bg"]

        )

        frame.pack(

            fill="x",

            padx=20

        )

        self.today_card = self.create_card(
            frame,
            "Today's Expense"
        )

        self.month_card = self.create_card(
            frame,
            "Monthly Expense"
        )

        self.total_card = self.create_card(
            frame,
            "Total Expense"
        )

        self.record_card = self.create_card(
            frame,
            "Records"
        )

    # ----------------------------------------------------

    def create_card(self, parent, title):

        card = tk.Frame(

            parent,

            width=220,

            height=95,

            bg="white",

            bd=1,

            relief="solid"

        )

        card.pack(

            side="left",

            padx=12

        )

        tk.Label(

            card,

            text=title,

            bg="white",

            font=("Segoe UI", 11)

        ).pack(

            pady=(12, 0)

        )

        value = tk.Label(

            card,

            text="₹0",

            bg="white",

            font=("Segoe UI", 18, "bold")

        )

        value.pack()

        return value

    # ----------------------------------------------------

    def create_search(self):

        top = tk.Frame(

            self.main,

            bg=self.theme["bg"]

        )

        top.pack(

            fill="x",

            padx=20,

            pady=12

        )

        self.search_var = tk.StringVar()

        tk.Entry(

            top,

            textvariable=self.search_var,

            width=35,

            font=NORMAL_FONT

        ).pack(

            side="left"

        )

        ttk.Button(

            top,

            text="Search",

            command=self.search

        ).pack(

            side="left",

            padx=10

        )

        ttk.Button(

            top,

            text="Refresh",

            command=self.refresh_dashboard

        ).pack(

            side="left"

        )

    # ----------------------------------------------------

    def create_table(self):

        columns = (

            "Date",

            "Expense",

            "Category",

            "Amount",

            "Payment",

            "Notes"

        )

        table_frame = tk.Frame(

            self.main,

            bg=self.theme["bg"]

        )

        table_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=10

        )

        scrollbar = ttk.Scrollbar(
            table_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree = ttk.Treeview(

            table_frame,

            columns=columns,

            show="headings",

            yscrollcommand=scrollbar.set

        )

        scrollbar.config(
            command=self.tree.yview
        )

        for col in columns:

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=150,
                anchor="center"
            )

        self.tree.pack(

            fill="both",

            expand=True
        )
    

        # ----------------------------------------------------

    def create_bottom_buttons(self):

        bottom = tk.Frame(
            self.main,
            bg=self.theme["bg"]
        )

        bottom.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Button(
            bottom,
            text="➕ Add Expense",
            command=self.open_add_expense
        ).pack(side="left")

        ttk.Button(
            bottom,
            text="🗑 Delete Selected",
            command=self.delete_selected
        ).pack(side="left", padx=10)

        ttk.Button(
            bottom,
            text="🔄 Refresh",
            command=self.refresh_dashboard
        ).pack(side="left")

    # ----------------------------------------------------

    def create_status(self):

        self.status = tk.Label(
            self.main,
            text="Ready",
            bg="#dddddd",
            anchor="w"
        )

        self.status.pack(
            fill="x",
            side="bottom"
        )

    # ----------------------------------------------------

    def load_table(self):

        self.tree.delete(*self.tree.get_children())

        expenses = self.manager.get_all_expenses()

        for expense in expenses:

            self.tree.insert(
                "",
                tk.END,
                values=(
                    expense["Date"],
                    expense["Expense"],
                    expense["Category"],
                    money(expense["Amount"]),
                    expense["Payment"],
                    expense["Notes"]
                )
            )

        self.today_card.config(
            text=money(self.manager.today_total())
        )

        self.month_card.config(
            text=money(self.manager.monthly_total())
        )

        self.total_card.config(
            text=money(self.manager.total_expense())
        )

        self.record_card.config(
            text=str(self.manager.total_records())
        )

        self.status.config(
            text=f"Loaded {self.manager.total_records()} expenses."
        )

    # ----------------------------------------------------

    def refresh_dashboard(self):

        self.load_table()

    # ----------------------------------------------------

    def search(self):

        keyword = self.search_var.get().strip()

        self.tree.delete(*self.tree.get_children())

        results = self.manager.search(keyword)

        for expense in results:

            self.tree.insert(
                "",
                tk.END,
                values=(
                    expense["Date"],
                    expense["Expense"],
                    expense["Category"],
                    money(expense["Amount"]),
                    expense["Payment"],
                    expense["Notes"]
                )
            )

        self.status.config(
            text=f"{len(results)} record(s) found."
        )

    # ----------------------------------------------------

    def delete_selected(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select an expense."
            )

            return

        index = self.tree.index(selected[0])

        if not messagebox.askyesno(
            "Delete",
            "Delete selected expense?"
        ):
            return

        self.manager.delete_expense(index)

        self.refresh_dashboard()

    # ----------------------------------------------------

    def open_add_expense(self):

        try:

            from add_expense import AddExpenseWindow

            AddExpenseWindow(
                self.root,
                self.refresh_dashboard
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ----------------------------------------------------


    # ----------------------------------------------------

    def logout(self):

        self.root.destroy()

        from login import LoginWindow

        LoginWindow()