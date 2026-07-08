# 💰 Expense Tracker (Python CLI)

A simple, dependency-free command-line application to track daily expenses.
Built with pure Python and the standard library only — no installs required.

Expenses are stored locally in a JSON file, so your data persists every time
you run the program.

---

## ✨ Features

- ➕ Add expenses with date, category, amount, and an optional note
- 📋 View all expenses in a clean tabular format
- 🔍 Filter expenses by category or by month (`YYYY-MM`)
- 📊 Category-wise spending summary
- 📅 Month-wise spending summary
- 🗑️ Delete an expense by ID
- 📤 Export all expenses to a CSV file (great for opening in Excel/Sheets)
- 💾 Data persists automatically between runs (`expenses.json`)

---

## 🖥️ Demo

```
========== EXPENSE TRACKER ==========
1. Add expense
2. View all expenses
3. View expenses by category
4. View expenses by month
5. Category-wise summary
6. Monthly summary
7. Delete expense
8. Export to CSV
9. Exit
======================================

Choose an option (1-9): 1
Date (YYYY-MM-DD) [Enter = today]:
Category (e.g. Food, Travel, Rent): Food
Amount: 250
Note (optional): Lunch with friends
Added expense #1: Food - ₹250.0
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher (no external packages needed)

### Run it

```bash
git clone https://github.com/<your-username>/expense-tracker.git
cd expense-tracker
python3 expense_tracker.py
```

That's it — no `pip install` required.

---

## 📁 Project Structure

```
expense-tracker/
├── expense_tracker.py   # Main application (CLI + logic)
├── expenses.json        # Auto-generated data file (created on first run)
└── README.md
```

---

## 🧠 How It Works

The project separates concerns into three layers:

| Layer | Responsibility |
|---|---|
| `Expense` (dataclass) | Represents a single expense record |
| `ExpenseTracker` | Handles storage, filtering, and calculations |
| `main()` / CLI helpers | Handles user interaction (menu, input, printing) |

All expenses are stored as plain JSON, making the data easy to inspect,
back up, or migrate elsewhere later (e.g. into a database or web app).

---

## 🛣️ Possible Future Improvements

- [ ] Add a budget limit with warnings when exceeded
- [ ] Add expense editing (not just delete + re-add)
- [ ] Support multiple currencies
- [ ] Add a simple bar chart of spending (matplotlib)
- [ ] Migrate storage to SQLite for larger datasets
- [ ] Build a Flask/Django web UI on top of the same `ExpenseTracker` class

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
