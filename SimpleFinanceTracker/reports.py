"""
reports.py
----------
Reports Window
- Monthly summary (table + line chart of daily spending)
- Category breakdown (pie chart)
- Export to CSV summary
- Uses: tkinter, matplotlib, numpy, pandas
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

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
    EXPENSE_FILE,
    money
)


class ReportsWindow:

    def __init__(self, parent):

        self.theme = get_theme()
        self.window = tk.Toplevel(parent)
        self.window.title("Reports")
        self.window.geometry("1100x700")
        self.window.configure(bg=self.theme["bg"])
        self.window.resizable(True, True)

        self._center_window()
        self._load_data()
        self._create_ui()

    # --------------------------------------------------

    def _center_window(self):

        w, h = 1100, 700
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")

    # --------------------------------------------------

    def _load_data(self):
        """Load and process all expense data using pandas."""

        try:
            self.df = pd.read_csv(EXPENSE_FILE)
            self.df["Amount"] = pd.to_numeric(
                self.df["Amount"], errors="coerce"
            ).fillna(0)
            self.df["Date"] = pd.to_datetime(
                self.df["Date"], format="%d-%m-%Y", errors="coerce"
            )
            self.df.dropna(subset=["Date"], inplace=True)

        except Exception:
            self.df = pd.DataFrame(
                columns=["Date", "Expense", "Category", "Amount", "Payment", "Notes"]
            )

        # Available months for dropdown
        if not self.df.empty:
            self.df["YearMonth"] = self.df["Date"].dt.to_period("M")
            months = self.df["YearMonth"].unique()
            self.month_options = sorted(
                [str(m) for m in months], reverse=True
            )
        else:
            self.month_options = []

        self.selected_month = tk.StringVar()
        if self.month_options:
            self.selected_month.set(self.month_options[0])

    # --------------------------------------------------

    def _create_ui(self):

        # ---- Header ----
        header = tk.Frame(self.window, bg=self.theme["primary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📄  Expense Reports",
            font=TITLE_FONT,
            bg=self.theme["primary"],
            fg="white"
        ).pack(side="left", padx=20, pady=12)

        # ---- Controls ----
        ctrl = tk.Frame(self.window, bg=self.theme["bg"])
        ctrl.pack(fill="x", padx=20, pady=10)

        tk.Label(
            ctrl,
            text="Select Month:",
            font=NORMAL_FONT,
            bg=self.theme["bg"]
        ).pack(side="left")

        if self.month_options:
            month_cb = ttk.Combobox(
                ctrl,
                textvariable=self.selected_month,
                values=self.month_options,
                width=15,
                state="readonly"
            )
            month_cb.pack(side="left", padx=8)
        else:
            tk.Label(
                ctrl,
                text="No data available",
                font=NORMAL_FONT,
                bg=self.theme["bg"],
                fg=self.theme["danger"]
            ).pack(side="left", padx=8)

        ttk.Button(
            ctrl,
            text="Generate Report",
            command=self._generate_report
        ).pack(side="left", padx=8)

        ttk.Button(
            ctrl,
            text="Export CSV",
            command=self._export_csv
        ).pack(side="left", padx=4)

        ttk.Button(
            ctrl,
            text="Close",
            command=self.window.destroy
        ).pack(side="right", padx=8)

        # ---- Main content area ----
        self.content = tk.Frame(self.window, bg=self.theme["bg"])
        self.content.pack(fill="both", expand=True, padx=15, pady=5)

        if self.month_options:
            self._generate_report()
        else:
            tk.Label(
                self.content,
                text="No expense records found.\nAdd some expenses first.",
                font=HEADER_FONT,
                bg=self.theme["bg"],
                fg="#9CA3AF"
            ).pack(expand=True)

    # --------------------------------------------------

    def _get_month_df(self):
        """Return DataFrame filtered to selected month."""

        month_str = self.selected_month.get()

        if not month_str or self.df.empty:
            return pd.DataFrame()

        period = pd.Period(month_str, freq="M")
        mask = self.df["YearMonth"] == period
        return self.df[mask].copy()

    # --------------------------------------------------

    def _generate_report(self):
        """Build all charts and tables for selected month."""

        # Clear old content
        for widget in self.content.winfo_children():
            widget.destroy()

        month_df = self._get_month_df()

        # ---- Summary cards row ----
        cards_row = tk.Frame(self.content, bg=self.theme["bg"])
        cards_row.pack(fill="x", pady=(5, 10))

        if month_df.empty:
            total = avg = top_amt = 0
            top_cat = "N/A"
            count = 0
        else:
            total = float(month_df["Amount"].sum())
            avg = float(month_df["Amount"].mean())
            count = len(month_df)
            cat_grp = month_df.groupby("Category")["Amount"].sum()
            top_cat = str(cat_grp.idxmax())
            top_amt = float(cat_grp.max())

        self._stat_card(cards_row, "Total Spent",   money(total),          self.theme["danger"])
        self._stat_card(cards_row, "Transactions",  str(count),            self.theme["primary"])
        self._stat_card(cards_row, "Avg per Entry", money(avg),            self.theme["secondary"])
        self._stat_card(cards_row, "Top Category",  f"{top_cat}\n{money(top_amt)}", "#7C3AED")

        # ---- Two-column layout ----
        columns = tk.Frame(self.content, bg=self.theme["bg"])
        columns.pack(fill="both", expand=True)

        # Left column
        left = tk.Frame(columns, bg=self.theme["bg"])
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Right column
        right = tk.Frame(columns, bg=self.theme["bg"])
        right.pack(side="right", fill="both", expand=True)

        self._draw_line_chart(left, month_df)
        self._draw_pie_chart(right, month_df)
        self._draw_table(right, month_df)

    # --------------------------------------------------

    def _stat_card(self, parent, title, value, color):

        card = tk.Frame(parent, bg="white", bd=1, relief="solid", width=220, height=75)
        card.pack(side="left", padx=6)
        card.pack_propagate(False)

        tk.Label(card, text=title, font=SMALL_FONT, bg="white", fg="#6B7280").pack(pady=(8, 0))
        tk.Label(card, text=value, font=("Segoe UI", 13, "bold"), bg="white", fg=color).pack()

    # --------------------------------------------------

    def _draw_line_chart(self, parent, month_df):
        """Daily spending line chart using matplotlib + numpy."""

        frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
        frame.pack(fill="both", expand=True, pady=(0, 8))

        tk.Label(
            frame,
            text="Daily Spending Trend",
            font=HEADER_FONT,
            bg="white"
        ).pack(pady=(10, 0))

        if month_df.empty:
            tk.Label(
                frame, text="No data", font=NORMAL_FONT,
                bg="white", fg="#9CA3AF"
            ).pack(expand=True)
            return

        daily = month_df.groupby(month_df["Date"].dt.day)["Amount"].sum()
        days = np.array(daily.index, dtype=int)
        amounts = np.array(daily.values, dtype=float)

        fig = Figure(figsize=(5, 3), dpi=95, facecolor="white")
        ax = fig.add_subplot(111)

        ax.plot(days, amounts, color=self.theme["primary"], linewidth=2,
                marker="o", markersize=5)
        ax.fill_between(days, amounts, alpha=0.12, color=self.theme["primary"])

        ax.set_xlabel("Day of Month", fontsize=9)
        ax.set_ylabel("Amount (₹)", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"₹{x:,.0f}")
        )
        ax.set_title(f"Daily Spending — {self.selected_month.get()}", fontsize=10, fontweight="bold")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    # --------------------------------------------------

    def _draw_pie_chart(self, parent, month_df):
        """Category pie chart."""

        frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
        frame.pack(fill="x", pady=(0, 8))

        tk.Label(
            frame,
            text="Category Breakdown",
            font=HEADER_FONT,
            bg="white"
        ).pack(pady=(10, 0))

        if month_df.empty:
            tk.Label(
                frame, text="No data", font=NORMAL_FONT,
                bg="white", fg="#9CA3AF"
            ).pack(pady=20)
            return

        cat_data = month_df.groupby("Category")["Amount"].sum()
        labels = list(cat_data.index)
        values = np.array(cat_data.values, dtype=float)

        fig = Figure(figsize=(5, 2.8), dpi=95, facecolor="white")
        ax = fig.add_subplot(111)

        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=plt.cm.Set2(np.linspace(0, 1, len(labels)))
        )

        for text in texts:
            text.set_fontsize(8)
        for at in autotexts:
            at.set_fontsize(7)

        ax.set_title("Expense Distribution", fontsize=10, fontweight="bold")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=8, pady=5)

    # --------------------------------------------------

    def _draw_table(self, parent, month_df):
        """Top 8 expenses table."""

        frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Top Expenses",
            font=HEADER_FONT,
            bg="white"
        ).pack(pady=(10, 4))

        cols = ("Date", "Expense", "Category", "Amount")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=6)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        if not month_df.empty:
            top = month_df.nlargest(8, "Amount")
            for _, row in top.iterrows():
                tree.insert("", tk.END, values=(
                    row["Date"].strftime("%d-%m-%Y"),
                    row["Expense"],
                    row["Category"],
                    f"₹ {row['Amount']:,.2f}"
                ))

        sb = ttk.Scrollbar(frame, command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=(0, 8))
        sb.pack(side="right", fill="y", pady=(0, 8), padx=(0, 4))

    # --------------------------------------------------

    def _export_csv(self):
        """Export selected month's data as a summary CSV using pandas."""

        month_df = self._get_month_df()

        if month_df.empty:
            messagebox.showwarning(
                "No Data",
                "No expenses found for the selected month.",
                parent=self.window
            )
            return

        path = filedialog.asksaveasfilename(
            parent=self.window,
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile=f"report_{self.selected_month.get()}.csv"
        )

        if not path:
            return

        # Build summary
        summary = month_df.groupby("Category").agg(
            Total_Spent=("Amount", "sum"),
            Transactions=("Amount", "count"),
            Average=("Amount", "mean")
        ).reset_index()

        summary = summary.round(2)
        summary.to_csv(path, index=False)

        messagebox.showinfo(
            "Exported",
            f"Report saved to:\n{path}",
            parent=self.window
        )
