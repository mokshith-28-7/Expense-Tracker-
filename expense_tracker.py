import json
from datetime import datetime

# Color support
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# Optional Matplotlib for charts
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

FILENAME = "expenses.txt"

# --- Load expenses ---
def load_expenses():
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# --- Save expenses ---
def save_expenses(expenses):
    with open(FILENAME, "w") as f:
        json.dump(expenses, f, indent=4)

# --- Add expense ---
def add_expense(expenses):
    try:
        amount = float(input(Fore.CYAN + "Enter amount: "))
    except ValueError:
        print(Fore.RED + "Invalid input! Amount must be a number.\n")
        return
    category = input(Fore.CYAN + "Enter category: ").strip()
    description = input(Fore.CYAN + "Enter description: ").strip()
    date_input = input(Fore.CYAN + "Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if date_input == "":
        date_input = str(datetime.today().date())

    expenses.append({
        "amount": amount,
        "category": category,
        "description": description,
        "date": date_input
    })
    save_expenses(expenses)
    print(Fore.GREEN + "Expense added successfully!\n")

# --- View all expenses ---
def view_expenses(expenses):
    if not expenses:
        print(Fore.YELLOW + "No expenses found.\n")
        return
    print(Fore.MAGENTA + "\nAll Expenses:")
    print("-"*60)
    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp['date']} | {exp['category']} | ₹{exp['amount']} | {exp['description']}")
    print("-"*60 + "\n")

# --- Total spending ---
def total_expenses(expenses):
    total = sum(exp["amount"] for exp in expenses)
    print(Fore.MAGENTA + f"Total Spending: ₹{total}\n")

# --- Expenses by category ---
def category_expenses(expenses):
    category = input(Fore.CYAN + "Enter category: ").strip()
    filtered = [exp for exp in expenses if exp["category"].lower() == category.lower()]
    if not filtered:
        print(Fore.YELLOW + f"No expenses found in '{category}'\n")
        return
    print(Fore.MAGENTA + f"\nExpenses in '{category}':")
    print("-"*60)
    for i, exp in enumerate(filtered, 1):
        print(f"{i}. {exp['date']} | ₹{exp['amount']} | {exp['description']}")
    print("-"*60 + "\n")

# --- Pie chart ---
def plot_pie(expenses):
    if not MATPLOTLIB_AVAILABLE:
        print(Fore.RED + "Matplotlib not installed. Cannot display chart.\n")
        return
    if not expenses:
        print(Fore.YELLOW + "No expenses to plot.\n")
        return
    categories = {}
    for exp in expenses:
        categories[exp["category"]] = categories.get(exp["category"], 0) + exp["amount"]
    plt.figure(figsize=(6,6))
    plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("Spending by Category")
    plt.show()

# --- Monthly bar chart ---
def plot_monthly(expenses):
    if not MATPLOTLIB_AVAILABLE:
        print(Fore.RED + "Matplotlib not installed. Cannot display chart.\n")
        return
    if not expenses:
        print(Fore.YELLOW + "No expenses to plot.\n")
        return
    monthly_totals = {}
    for exp in expenses:
        try:
            month = datetime.strptime(exp["date"], "%Y-%m-%d").strftime("%Y-%m")
        except ValueError:
            continue
        monthly_totals[month] = monthly_totals.get(month, 0) + exp["amount"]
    months = sorted(monthly_totals.keys())
    amounts = [monthly_totals[m] for m in months]
    plt.figure(figsize=(8,5))
    plt.bar(months, amounts, color='skyblue')
    plt.xlabel("Month")
    plt.ylabel("Total Spending (₹)")
    plt.title("Monthly Spending")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# --- Main menu ---
def main():
    expenses = load_expenses()
    while True:
        print(Fore.GREEN + "="*40)
        print(Fore.CYAN + "        EXPENSE TRACKER MENU        ")
        print(Fore.GREEN + "="*40)
        print(Fore.YELLOW + "1. Add Expense")
        print("2. View All Expenses")
        print("3. Total Spending")
        print("4. View by Category")
        if MATPLOTLIB_AVAILABLE:
            print("5. Show Pie Chart")
            print("6. Show Monthly Bar Chart")
            print("7. Exit")
        else:
            print("5. Exit (Charts unavailable)")

        choice = input(Fore.CYAN + "Enter choice: ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            total_expenses(expenses)
        elif choice == "4":
            category_expenses(expenses)
        elif choice == "5":
            if MATPLOTLIB_AVAILABLE:
                plot_pie(expenses)
            else:
                print(Fore.GREEN + "Goodbye!")
                break
        elif choice == "6" and MATPLOTLIB_AVAILABLE:
            plot_monthly(expenses)
        elif choice == "7" and MATPLOTLIB_AVAILABLE:
            print(Fore.GREEN + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice! Try again.\n")

if __name__ == "__main__":
    main()