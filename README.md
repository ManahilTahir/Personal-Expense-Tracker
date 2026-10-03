# Final Expense Tracker

A simple and beginner-friendly desktop application to track personal expenses, built using **Python** and **Tkinter** only. No external libraries are required.

## Features

- Add an expense with **Date**, **Category**, **Description**, and **Amount**.
- Predefined categories: Food, Transport, Shopping, Bills, Education, Health, Other.
- **Live expense list** on the main window — added expenses appear immediately.
- **Update Expense** — select an expense and change its date, category, description, or amount.
- **Currency selector** — choose between USD, PKR, AED, EUR, GBP, INR, SAR. Totals and the list update instantly.
- **Custom logo** (`logo.png`) generated with pure Python — shown in the header and used as the window/taskbar icon.
- **Footer** crediting the developer.
- View all expenses in a clean table (`ttk.Treeview`).
- Search expenses by **date**, **category**, or **description**.
- Delete a selected expense with confirmation.
- Automatically updates **Total Expenses** and **Number of Expenses**.
- Validates empty fields and invalid amounts.
- Expenses and currency preference are saved to `expenses.json` and loaded automatically on startup.

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
| `logo.png`       | App logo, auto-generated on first run.   |
| `expenses.json`  | Stores expenses + currency (auto-created). |
| `README.md`      | This documentation file.                 |

## GUI Overview

- A custom **logo** (`logo.png`) generated entirely with Python (pure PNG encoding via `struct` + `zlib`) — a green circle with a gold ring and a white `$`. Shown in the header and used as the window/taskbar icon.
- Centered, colored heading: **Final Expense Tracker**.
- Stats panel showing total expenses and count, plus a currency dropdown.
- Buttons: Add Expense, View Expenses, Search Expense, Update Expense, Delete Expense, Exit.
- A live expense list table below the buttons.
- Footer: **developed by : Manahil Tahir**.

## Notes

- If `expenses.json` does not exist, it is created automatically when the first expense is added.
- The application uses simple `try/except` blocks to handle file and input errors gracefully.
