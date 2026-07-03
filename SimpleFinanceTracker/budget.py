"""
budget.py
---------
Budget Management Window
- Set monthly budget
- View budget vs actual spending (progress bar + chart)
- Uses: tkinter, matplotlib, numpy, pandas
"""

import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime

from helpers import (
    get_theme,
    TITLE_FONT,
    HEADER_FONT,
    NORMAL_FONT,
    SMALL_FONT,
    BUDGET_FILE,
    EXPENSE_FILE,
    read_json,
    write_json,
    money
)


class BudgetWindow:

    def __init__(self, parent):

        self.theme = get_theme()
        self.window = tk.Toplevel(parent)
        self.window.title("Budget Manager")
        self.window.geometry("900x650")
        self.window.configure(bg=self.theme["bg"])
        self.window.resizable(False, False)

        self._center_window()
        self._load_data()
        self._create_ui()

    # --------------------------------------------------

    def _center_window(self):

        w, h = 900, 650
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")

    # --------------------------------------------------

    def _load_data(self):
        """Load budget and expense data using pandas."""

        budget_data = read_json(BUDGET_FILE)
        self.monthly_budget = float(budget_data.get("monthly_budget", 10000))

        try:
            self.df = pd.read_csv(EXPENSE_FILE)
            self.df["Amount"] = pd.to_numeric(self.df["Amount"], errors="coerce").fillna(0)

            # Parse dates
            self.df["Date"] = pd.to_datetime(
                self.df["Date"], format="%d-%m-%Y", errors="coerce"
            )

        except Exception:
            self.df = pd.DataFrame(
                columns=["Date", "Expense", "Category", "Amount", "Payment", "Notes"]
            )

        # Current month filter
        now = datetime.now()
        self.current_month_label = now.strftime("%B %Y")
        mask = (
            (self.df["Date"].dt.month == now.month) &
            (self.df["Date"].dt.year == now.year)
        )
        self.month_df = self.df[mask]
        self.month_total = float(self.month_df["Amount"].sum())

        # Budget stats
        self.remaining = self.monthly_budget - self.month_total
        self.used_pct = (
            (self.month_total / self.monthly_budget * 100)
            if self.monthly_budget > 0 else 0
        )

    # --------------------------------------------------

    def _create_ui(self):

        # ---- Header ----
        header = tk.Frame(self.window, bg=self.theme["primary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="💰  Budget Manager",
            font=TITLE_FONT,
            bg=self.theme["primary"],
            fg="white"
        ).pack(side="left", padx=20, pady=12)

        tk.Label(
            header,
            text=self.current_month_label,
            font=HEADER_FONT,
            bg=self.theme["primary"],
            fg="white"
        ).pack(side="right", padx=20)

        # ---- Top cards row ----
        cards_row = tk.Frame(self.window, bg=self.theme["bg"])
        cards_row.pack(fill="x", padx=20, pady=15)

        self._stat_card(cards_row, "Monthly Budget",  money(self.monthly_budget),  self.theme["primary"])
        self._stat_card(cards_row, "Amount Spent",    money(self.month_total),     self.theme["danger"])
        self._stat_card(cards_row, "Remaining",       money(max(self.remaining, 0)), self.theme["success"])
        self._stat_card(cards_row, "Used %",          f"{min(self.used_pct, 100):.1f}%",
                        self.theme["danger"] if self.used_pct > 90 else self.theme["primary"])

        # ---- Progress bar section ----
        prog_frame = tk.Frame(
            self.window, bg="white", bd=1, relief="solid"
        )
        prog_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            prog_frame,
            text="Budget Usage",
            font=HEADER_FONT,
            bg="white"
        ).pack(anchor="w", padx=15, pady=(10, 4))

        pct = min(self.used_pct, 100)
        color = "#EF4444" if pct > 90 else ("#F59E0B" if pct > 70 else "#22C55E")

        bar_bg = tk.Frame(prog_frame, bg="#E5E7EB", height=28)
        bar_bg.pack(fill="x", padx=15, pady=(0, 5))
        bar_bg.pack_propagate(False)

        if pct > 0:
            fill = tk.Frame(bar_bg, bg=color, height=28)
            fill.place(relx=0, rely=0, relwidth=pct / 100, relheight=1)

        tk.Label(
            prog_frame,
            text=f"₹ {self.month_total:,.2f}  /  ₹ {self.monthly_budget:,.2f}",
            font=NORMAL_FONT,
            bg="white",
            fg="#6B7280"
        ).pack(anchor="e", padx=15, pady=(0, 10))

        # ---- Bottom: chart + set budget ----
        bottom = tk.Frame(self.window, bg=self.theme["bg"])
        bottom.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: chart
        chart_frame = tk.Frame(bottom, bg="white", bd=1, relief="solid")
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self._draw_chart(chart_frame)

        # Right: set budget + category table
        right_frame = tk.Frame(bottom, bg=self.theme["bg"])
        right_frame.pack(side="right", fill="both", expand=True)

        self._create_set_budget_panel(right_frame)
        self._create_category_table(right_frame)

    # --------------------------------------------------

    def _stat_card(self, parent, title, value, color):

        card = tk.Frame(parent, bg="white", bd=1, relief="solid", width=190, height=80)
        card.pack(side="left", padx=8)
        card.pack_propagate(False)

        tk.Label(card, text=title, font=SMALL_FONT, bg="white", fg="#6B7280").pack(pady=(10, 0))
        tk.Label(card, text=value, font=("Segoe UI", 15, "bold"), bg="white", fg=color).pack()

    # --------------------------------------------------

    def _draw_chart(self, parent):
        """Bar chart: Budget vs Spent for each category using matplotlib + numpy."""

        tk.Label(
            parent,
            text="Category Spending",
            font=HEADER_FONT,
            bg="white"
        ).pack(pady=(10, 0))

        if self.month_df.empty:
            tk.Label(
                parent,
                text="No data for this month",
                font=NORMAL_FONT,
                bg="white",
                fg="#9CA3AF"
            ).pack(expand=True)
            return

        cat_totals = self.month_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

        categories = list(cat_totals.index)
        amounts = np.array(cat_totals.values, dtype=float)

        fig = Figure(figsize=(5, 3.5), dpi=95, facecolor="white")
        ax = fig.add_subplot(111)

        colors = plt.cm.Set2(np.linspace(0, 1, len(categories)))
        bars = ax.barh(categories, amounts, color=colors, edgecolor="none")

        ax.set_xlabel("Amount (₹)", fontsize=9)
        ax.set_title("Spending by Category", fontsize=11, fontweight="bold", pad=8)
        ax.tick_params(labelsize=8)
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"₹{x:,.0f}")
        )

        for bar, val in zip(bars, amounts):
            ax.text(
                bar.get_width() + max(amounts) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}",
                va="center",
                fontsize=8
            )

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    # --------------------------------------------------

    def _create_set_budget_panel(self, parent):

        panel = tk.Frame(parent, bg="white", bd=1, relief="solid")
        panel.pack(fill="x", pady=(0, 10))

        tk.Label(
            panel,
            text="Set Monthly Budget",
            font=HEADER_FONT,
            bg="white"
        ).pack(pady=(10, 5))

        row = tk.Frame(panel, bg="white")
        row.pack(padx=15, pady=(0, 15))

        tk.Label(row, text="₹", font=("Segoe UI", 14, "bold"), bg="white").pack(side="left")

        self.budget_entry = ttk.Entry(row, width=14, font=NORMAL_FONT)
        self.budget_entry.insert(0, str(int(self.monthly_budget)))
        self.budget_entry.pack(side="left", padx=5)

        ttk.Button(
            row,
            text="Save",
            command=self._save_budget
        ).pack(side="left")

    # --------------------------------------------------

    def _create_category_table(self, parent):

        frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="This Month — Category Summary",
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(pady=(10, 5))

        cols = ("Category", "Spent")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=6)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=130)

        if not self.month_df.empty:
            cat_series = self.month_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            for cat, total in cat_series.items():
                tree.insert("", tk.END, values=(cat, f"₹ {total:,.2f}"))

        tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # --------------------------------------------------

    def _save_budget(self):

        val = self.budget_entry.get().strip()

        try:
            amount = float(val)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive amount.", parent=self.window)
            return

        write_json(BUDGET_FILE, {"monthly_budget": amount})

        messagebox.showinfo("Saved", f"Monthly budget set to ₹ {amount:,.2f}", parent=self.window)

        # Refresh
        self.window.destroy()
