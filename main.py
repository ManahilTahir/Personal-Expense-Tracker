import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Education", "Health", "Other"]
CURRENCIES = {"USD": "$", "PKR": "Rs", "AED": "AED", "EUR": "€", "GBP": "£", "INR": "₹", "SAR": "SAR"}

HEADER_BG = "#1a1a2e"
ACCENT = "#f1c40f"


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Final Expense Tracker")
        self.root.geometry("780x600")
        self.root.resizable(False, False)

        self.expenses = []
        self.currency = "USD"
        self.load_expenses()

        self.build_header()
        self.build_stats()
        self.build_buttons()
        self.build_list()

    def build_header(self):
        header = tk.Frame(self.root, bg=HEADER_BG)
        header.pack(fill="x")

        center = tk.Frame(header, bg=HEADER_BG)
        center.pack(anchor="center", pady=8)

        self.logo_canvas = tk.Canvas(center, width=56, height=56, bg=HEADER_BG, highlightthickness=0)
        self.logo_canvas.pack(side="left", padx=10)
        self.draw_logo()

        tk.Label(
            center,
            text="Final Expense Tracker",
            font=("Helvetica", 22, "bold"),
            fg=ACCENT,
            bg=HEADER_BG,
        ).pack(side="left", padx=10)

        tk.Label(
            header,
            text="Track  •  Manage  •  Save",
            font=("Helvetica", 10, "italic"),
            fg="#95a5a6",
            bg=HEADER_BG,
        ).pack(anchor="center", pady=(0, 8))

    def draw_logo(self):
        self.logo_canvas.delete("all")
        sym = CURRENCIES.get(self.currency, "$")
        size = 22 if len(sym) == 1 else (15 if len(sym) == 2 else 12)
        self.logo_canvas.create_oval(4, 4, 52, 52, fill="#27ae60", outline=ACCENT, width=2)
        self.logo_canvas.create_text(28, 28, text=sym, font=("Helvetica", size, "bold"), fill="white")

    def build_stats(self):
        stats = tk.Frame(self.root, bg="#ecf0f1")
        stats.pack(fill="x", pady=5)

        self.total_label = tk.Label(stats, text="Total Expenses: $0.00", font=("Helvetica", 12, "bold"), bg="#ecf0f1", fg="#2c3e50")
        self.total_label.pack(side="left", padx=20, pady=8)

        self.count_label = tk.Label(stats, text="Number of Expenses: 0", font=("Helvetica", 12, "bold"), bg="#ecf0f1", fg="#2c3e50")
        self.count_label.pack(side="left", padx=20, pady=8)

        self.currency_var = tk.StringVar(value=self.currency)
        ttk.Combobox(stats, textvariable=self.currency_var, values=list(CURRENCIES.keys()), state="readonly", width=8, font=("Helvetica", 11)).pack(side="right", padx=(5, 20), pady=8)
        tk.Label(stats, text="Currency:", font=("Helvetica", 11, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(side="right", pady=8)
        self.currency_var.trace_add("write", self.on_currency_change)

        self.update_stats()

    def build_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(fill="x", pady=5)

        buttons = [
            ("Add Expense", "#27ae60", "#229954", self.add_expense),
            ("View Expenses", "#3498db", "#2980b9", self.view_expenses),
            ("Search Expense", "#9b59b6", "#8e44ad", self.search_expense),
            ("Update Expense", "#f39c12", "#d68910", self.update_expense),
            ("Delete Expense", "#e74c3c", "#c0392b", self.delete_expense),
            ("Exit", "#7f8c8d", "#616e70", self.root.quit),
        ]

        for text, bg, active, cmd in buttons:
            tk.Button(
                btn_frame,
                text=text,
                font=("Helvetica", 11, "bold"),
                width=13,
                bg=bg,
                fg="white",
                activebackground=active,
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=cmd,
            ).pack(side="left", padx=6, pady=10)

    def build_list(self):
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        tk.Label(list_frame, text="Expense List", font=("Helvetica", 12, "bold"), fg="#2c3e50", anchor="w").pack(fill="x", pady=(0, 4))

        columns = ("Date", "Category", "Description", "Amount")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column("Date", width=110, anchor="center")
        self.tree.column("Category", width=110, anchor="center")
        self.tree.column("Description", width=300, anchor="w")
        self.tree.column("Amount", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_tree()

    def load_expenses(self):
        self.expenses = []
        self.currency = "USD"
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self.expenses = data.get("expenses", [])
                    self.currency = data.get("currency", "USD")
                elif isinstance(data, list):
                    self.expenses = data
        except Exception:
            self.expenses = []
            self.currency = "USD"

    def save_expenses(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump({"currency": self.currency, "expenses": self.expenses}, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save expenses:\n{e}")

    def format_amount(self, amount):
        sym = CURRENCIES.get(self.currency, "$")
        if len(sym) == 1:
            return f"{sym}{amount:.2f}"
        return f"{sym} {amount:.2f}"

    def update_stats(self):
        try:
            total = sum(float(e.get("amount", 0)) for e in self.expenses)
        except Exception:
            total = 0.0
        self.total_label.config(text=f"Total Expenses: {self.format_amount(total)}")
        self.count_label.config(text=f"Number of Expenses: {len(self.expenses)}")

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for idx, e in enumerate(self.expenses):
            self.tree.insert(
                "", "end", iid=idx,
                values=(e.get("date", ""), e.get("category", ""), e.get("description", ""), self.format_amount(float(e.get("amount", 0)))),
            )

    def on_currency_change(self, *args):
        self.currency = self.currency_var.get()
        self.save_expenses()
        self.draw_logo()
        self.update_stats()
        self.refresh_tree()

    def open_expense_form(self, existing_index=None):
        is_update = existing_index is not None
        existing = self.expenses[existing_index] if is_update else {}

        form = tk.Toplevel(self.root)
        form.title("Update Expense" if is_update else "Add Expense")
        form.geometry("340x320")
        form.resizable(False, False)
        form.grab_set()

        tk.Label(form, text="Date (YYYY-MM-DD):", font=("Helvetica", 10)).pack(pady=(15, 2))
        date_entry = tk.Entry(form, font=("Helvetica", 11))
        date_entry.insert(0, existing.get("date", datetime.now().strftime("%Y-%m-%d")))
        date_entry.pack(pady=2)

        tk.Label(form, text="Category:", font=("Helvetica", 10)).pack(pady=(5, 2))
        category_var = tk.StringVar(value=existing.get("category", CATEGORIES[0]))
        ttk.Combobox(form, textvariable=category_var, values=CATEGORIES, state="readonly", font=("Helvetica", 11)).pack(pady=2)

        tk.Label(form, text="Description:", font=("Helvetica", 10)).pack(pady=(5, 2))
        desc_entry = tk.Entry(form, font=("Helvetica", 11))
        desc_entry.insert(0, existing.get("description", ""))
        desc_entry.pack(pady=2)

        tk.Label(form, text="Amount:", font=("Helvetica", 10)).pack(pady=(5, 2))
        amount_entry = tk.Entry(form, font=("Helvetica", 11))
        if is_update:
            amount_entry.insert(0, str(existing.get("amount", "")))
        amount_entry.pack(pady=2)

        def save():
            date = date_entry.get().strip()
            category = category_var.get().strip()
            description = desc_entry.get().strip()
            amount = amount_entry.get().strip()

            if not date or not category or not description or not amount:
                messagebox.showwarning("Missing Fields", "Please fill in all fields.")
                return

            try:
                amount_val = float(amount)
                if amount_val <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Invalid Amount", "Amount must be a positive number.")
                return

            record = {"date": date, "category": category, "description": description, "amount": amount_val}
            if is_update:
                self.expenses[existing_index] = record
                msg = "Expense updated successfully."
            else:
                self.expenses.append(record)
                msg = "Expense added successfully."

            self.save_expenses()
            self.update_stats()
            self.refresh_tree()
            form.destroy()
            messagebox.showinfo("Success", msg)

        tk.Button(form, text="Save", font=("Helvetica", 11, "bold"), bg="#27ae60", fg="white", width=12, command=save).pack(pady=15)

    def add_expense(self):
        self.open_expense_form()

    def update_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an expense from the list to update.")
            return
        self.open_expense_form(int(selected[0]))

    def view_expenses(self):
        if not self.expenses:
            messagebox.showinfo("No Expenses", "There are no expenses to show.")
            return

        view = tk.Toplevel(self.root)
        view.title("View Expenses")
        view.geometry("640x420")
        view.grab_set()

        tree = ttk.Treeview(view, columns=("Date", "Category", "Description", "Amount"), show="headings")
        for col in ("Date", "Category", "Description", "Amount"):
            tree.heading(col, text=col)
        tree.column("Date", width=110, anchor="center")
        tree.column("Category", width=110, anchor="center")
        tree.column("Description", width=280, anchor="w")
        tree.column("Amount", width=120, anchor="center")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for e in self.expenses:
            tree.insert("", "end", values=(e.get("date", ""), e.get("category", ""), e.get("description", ""), self.format_amount(float(e.get("amount", 0)))))

    def search_expense(self):
        search = tk.Toplevel(self.root)
        search.title("Search Expense")
        search.geometry("320x180")
        search.resizable(False, False)
        search.grab_set()

        tk.Label(search, text="Search by:", font=("Helvetica", 10)).pack(pady=(15, 2))
        field_var = tk.StringVar(value="date")
        ttk.Combobox(search, textvariable=field_var, values=["date", "category", "description"], state="readonly", font=("Helvetica", 11)).pack(pady=2)

        tk.Label(search, text="Keyword:", font=("Helvetica", 10)).pack(pady=(5, 2))
        keyword_entry = tk.Entry(search, font=("Helvetica", 11))
        keyword_entry.pack(pady=2)

        def do_search():
            field = field_var.get()
            keyword = keyword_entry.get().strip().lower()
            if not keyword:
                messagebox.showwarning("Empty", "Please enter a keyword.")
                return

            results = [e for e in self.expenses if keyword in str(e.get(field, "")).lower()]
            search.destroy()

            if not results:
                messagebox.showinfo("No Results", "No matching expenses found.")
                return

            result_win = tk.Toplevel(self.root)
            result_win.title("Search Results")
            result_win.geometry("640x420")
            result_win.grab_set()

            tree = ttk.Treeview(result_win, columns=("Date", "Category", "Description", "Amount"), show="headings")
            for col in ("Date", "Category", "Description", "Amount"):
                tree.heading(col, text=col)
            tree.column("Date", width=110, anchor="center")
            tree.column("Category", width=110, anchor="center")
            tree.column("Description", width=280, anchor="w")
            tree.column("Amount", width=120, anchor="center")
            tree.pack(fill="both", expand=True, padx=10, pady=10)

            for e in results:
                tree.insert("", "end", values=(e.get("date", ""), e.get("category", ""), e.get("description", ""), self.format_amount(float(e.get("amount", 0)))))

        tk.Button(search, text="Search", font=("Helvetica", 11, "bold"), bg="#3498db", fg="white", width=12, command=do_search).pack(pady=15)

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an expense from the list to delete.")
            return

        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected expense?"):
            return

        for item in sorted(selected, reverse=True):
            del self.expenses[int(item)]
        self.save_expenses()
        self.update_stats()
        self.refresh_tree()
        messagebox.showinfo("Deleted", "Expense deleted successfully.")


def main():
    root = tk.Tk()
    ExpenseTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
