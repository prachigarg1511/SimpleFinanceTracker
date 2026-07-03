"""
helpers.py
------------
Common helper functions used throughout the project.
"""

import json
import os
from datetime import datetime

# ===========================
# DATABASE PATHS
# ===========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, "database")

EXPENSE_FILE = os.path.join(DATABASE_DIR, "expenses.csv")

USERS_FILE = os.path.join(DATABASE_DIR, "users.json")

BUDGET_FILE = os.path.join(DATABASE_DIR, "budget.json")

SETTINGS_FILE = os.path.join(DATABASE_DIR, "settings.json")


# ===========================
# COLORS
# ===========================

LIGHT_THEME = {

    "bg": "#EEF2F7",

    "card": "#FFFFFF",

    "primary": "#2563EB",

    "secondary": "#1E40AF",

    "success": "#22C55E",

    "danger": "#EF4444",

    "text": "#111827",

    "button_text": "#FFFFFF"

}

DARK_THEME = {

    "bg": "#1F2937",

    "card": "#374151",

    "primary": "#3B82F6",

    "secondary": "#60A5FA",

    "success": "#10B981",

    "danger": "#EF4444",

    "text": "#FFFFFF",

    "button_text": "#FFFFFF"

}


# ===========================
# FONT
# ===========================

TITLE_FONT = ("Segoe UI", 22, "bold")

HEADER_FONT = ("Segoe UI", 16, "bold")

NORMAL_FONT = ("Segoe UI", 11)

SMALL_FONT = ("Segoe UI", 10)


# ===========================
# DATE
# ===========================

def today():

    return datetime.now().strftime("%d-%m-%Y")


# ===========================
# JSON FUNCTIONS
# ===========================

def read_json(file_path):

    if not os.path.exists(file_path):

        return {}

    with open(file_path, "r") as file:

        try:

            return json.load(file)

        except:

            return {}


def write_json(file_path, data):

    with open(file_path, "w") as file:

        json.dump(data, file, indent=4)


# ===========================
# CREATE DATABASE FILES
# ===========================

def initialize_database():

    os.makedirs(DATABASE_DIR, exist_ok=True)

    if not os.path.exists(USERS_FILE):

        write_json(
            USERS_FILE,
            {
                "admin": "admin123"
            }
        )

    if not os.path.exists(BUDGET_FILE):

        write_json(
            BUDGET_FILE,
            {
                "monthly_budget": 10000
            }
        )

    if not os.path.exists(SETTINGS_FILE):

        write_json(
            SETTINGS_FILE,
            {
                "theme": "light"
            }
        )

    if not os.path.exists(EXPENSE_FILE):

        with open(EXPENSE_FILE, "w") as file:

            file.write(
                "Date,Expense,Category,Amount,Payment,Notes\n"
            )


# ===========================
# LOAD THEME
# ===========================

def get_theme():

    settings = read_json(SETTINGS_FILE)

    if settings.get("theme") == "dark":

        return DARK_THEME

    return LIGHT_THEME


# ===========================
# MONEY FORMAT
# ===========================

def money(value):

    return f"₹ {float(value):,.2f}"