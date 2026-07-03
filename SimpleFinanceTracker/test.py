from expense_manager import ExpenseManager
from helpers import today

manager = ExpenseManager()

manager.add_expense(
    today(),
    "Pizza",
    "Food",
    450,
    "UPI",
    "Dinner"
)

print(manager.get_all_expenses())
print("Total:", manager.total_expense())
print("Today's Total:", manager.today_total())