# Final Expense Tracker

A simple and beginner-friendly desktop application to track personal expenses, built using **Python** and **Tkinter** only. No external libraries are required.

## Features

- Add an expense with **Date**, **Category**, **Description**, and **Amount**.
- Predefined categories: Food, Transport, Shopping, Bills, Education, Health, Other.
- View all expenses in a clean table (`ttk.Treeview`).
- Search expenses by **date**, **category**, or **description**.
- Delete a selected expense with confirmation.
- Automatically updates **Total Expenses** and **Number of Expenses**.
- Validates empty fields and invalid amounts.
- Expenses are saved to `expenses.json` and loaded automatically on startup.

## Requirements

- Python 3.x (Tkinter is included with standard Python installations).

## How to Run

```bash
python main.py
```

## Files

| File             | Description                              |
|------------------|------------------------------------------|
| `main.py`        | Main application code (Tkinter GUI).     |
| `expenses.json`  | Stores expenses data (auto-created).     |
| `README.md`      | This documentation file.                 |

## GUI Overview

- A money-related logo (green circle with `$`) drawn using Tkinter Canvas.
- Heading: **Final Expense Tracker**.
- Stats panel showing total expenses and count.
- Buttons: Add Expense, View Expenses, Search Expense, Delete Expense, Exit.

## Notes

- If `expenses.json` does not exist, it is created automatically when the first expense is added.
- The application uses simple `try/except` blocks to handle file and input errors gracefully.