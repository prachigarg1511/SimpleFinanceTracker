# 💰 Simple Finance Tracker

A desktop **personal finance tracking application** built with **Python**, **Tkinter**, and **Matplotlib**. It lets you log expenses, monitor budgets, visualise spending patterns, and export reports — all from a clean, modern GUI.

---

## 📸 Features at a Glance

| Feature | Description |
|---|---|
| 🔐 Login / Sign-up | Secure multi-user authentication stored locally |
| 🏠 Dashboard | Summary cards, searchable expense table, add/delete records |
| ➕ Add Expense | Log expenses with category, payment method, date, and notes |
| 📊 Analytics | Pie chart and bar chart of spending by category |
| 💰 Budget Manager | Set monthly budget, track usage with progress bar and category chart |
| 📄 Reports | Monthly line chart, pie chart, top-expenses table, CSV export |
| ⚙️ Settings | Toggle Light / Dark theme, change password |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| GUI | Tkinter + ttk |
| Charts | Matplotlib (FigureCanvasTkAgg) |
| Data Processing | Pandas, NumPy |
| Storage | CSV (expenses), JSON (users, budget, settings) |

---

## 📁 Project Structure

```
SimpleFinanceTracker/
│
├── main.py               # Entry point — initialises DB and launches login
├── login.py              # Login & Sign-up window
├── dashboard.py          # Main dashboard with sidebar navigation
├── add_expense.py        # Add Expense form window
├── analytics.py          # Pie chart + bar chart analytics window
├── budget.py             # Budget manager with progress bar & category chart
├── reports.py            # Monthly reports with line chart, pie chart & CSV export
├── settings.py           # Theme toggle & password change
├── expense_manager.py    # CRUD operations on expenses.csv
├── helpers.py            # Shared constants, themes, fonts, JSON helpers
│
└── database/
    ├── expenses.csv       # All expense records
    ├── users.json         # Registered users (username to password)
    ├── budget.json        # Saved monthly budget
    └── settings.json      # App settings (theme)
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites

Make sure you have **Python 3.8+** installed. Check with:

```bash
python --version
```

### 2. Install Required Libraries

```bash
pip install matplotlib pandas numpy
```

> **Note:** `tkinter` comes bundled with Python on Windows. No extra install needed.

### 3. Run the Application

```bash
python main.py
```

---

## 🚀 How to Use

### 🔐 Login
- Default credentials: **Username:** `admin` | **Password:** `admin123`
- Or create a new account directly from the login screen.

### 🏠 Dashboard
- View **Today's Expense**, **Monthly Expense**, **Total Expense**, and **Total Records** on summary cards.
- Search expenses by keyword.
- Add new expenses or delete selected ones.
- Use the sidebar to navigate to all features.

### ➕ Add Expense
Fill in:
- **Date** (auto-filled to today)
- **Expense Name**
- **Category** — Food, Travel, Shopping, Bills, Medical, Education, Entertainment, Office, Others
- **Amount**
- **Payment Method** — Cash, UPI, Card, Net Banking
- **Notes** (optional)

### 📊 Analytics
- **Pie Chart** — Spending share by category.
- **Bar Chart** — Category-wise comparison.
- Summary cards showing Total Expense, Highest Category, and Average.

### 💰 Budget Manager
- Set a monthly budget amount.
- Visual **progress bar** changes colour:
  - Green — under 70%
  - Yellow — 70–90%
  - Red — over 90%
- Horizontal bar chart of category-wise spending for the current month.
- Category summary table.

### 📄 Reports
- Select any past month from the dropdown.
- View a **daily spending line chart**, **category pie chart**, and a **top-8 expenses table**.
- **Export** the month's category summary as a `.csv` file.

### ⚙️ Settings
- Switch between **Light** and **Dark** themes (restart required to apply fully).
- Change your account password.

---

## 🗄️ Data Storage

All data is stored locally in the `database/` folder:

| File | Format | Contents |
|---|---|---|
| `expenses.csv` | CSV | All expense records |
| `users.json` | JSON | Username to password mapping |
| `budget.json` | JSON | Monthly budget value |
| `settings.json` | JSON | Current theme preference |

The `database/` folder and all required files are **auto-created** on first run via `helpers.initialize_database()`.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `tkinter` | GUI framework (built-in) |
| `matplotlib` | Charts and visualisations |
| `pandas` | Data loading, filtering, grouping |
| `numpy` | Numeric array processing for charts |

Install all at once:

```bash
pip install matplotlib pandas numpy
```

---

## 🎨 Themes

The app supports two built-in themes:

| Theme | Background | Primary Colour |
|---|---|---|
| Light | #EEF2F7 | #2563EB (Blue) |
| Dark | #1F2937 | #3B82F6 (Blue) |

Switch themes from **Settings → Appearance** and restart the app.

---

## 📝 Notes

- Expenses are stored in `DD-MM-YYYY` format.
- Passwords are stored in plain text in `users.json` — this is a local learning project and not intended for production use.
- The default monthly budget is **Rs. 10,000**; change it anytime from the Budget Manager.

---

## 👩‍💻 Author

**Prachi Garg**  
*Summer Training Project — Cybercore Technologies*  
Built with Python, Tkinter, and Matplotlib.

---

## 👥 Contributors

| Profile | Name | Description |
| :--- | :--- | :--- |
| <img src="https://github.com/prachigarg1511.png" width="100px;"/> | **Prachi Garg** | **Lead Architect & Full-Stack Developer**. Passionate about bridging the gap between Artificial Intelligence and Education. Built the core AI engine, gamification logic, and real time Synchronization. |

