import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Education", "Health", "Other"]


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Final Expense Tracker")
        self.root.geometry("700x520")
        self.root.resizable(False, False)

        self.expenses = []
        self.load_expenses()

        self.build_header()
        self.build_stats()
        self.build_buttons()

    def build_header(self):
        header = tk.Frame(self.root, bg="#2c3e50")
        header.pack(fill="x")

        self.draw_logo(header)

        tk.Label(
            header,
            text="Final Expense Tracker",
            font=("Helvetica", 20, "bold"),
            fg="white",
            bg="#2c3e50",
            pady=10,
        ).pack(side="left", padx=10)

    def draw_logo(self, parent):
        canvas = tk.Canvas(parent, width=60, height=60, bg="#2c3e50", highlightthickness=0)
        canvas.pack(side="left", padx=15, pady=10)
        canvas.create_oval(6, 6, 54, 54, fill="#27ae60", outline="white", width=2)
        canvas.create_text(30, 30, text="$", font=("Helvetica", 24, "bold"), fill="white")

    def build_stats(self):
        stats = tk.Frame(self.root, bg="#ecf0f1")
        stats.pack(fill="x", pady=10)

        self.total_label = tk.Label(stats, text="Total Expenses: $0.00", font=("Helvetica", 12, "bold"), bg="#ecf0f1", fg="#2c3e50")
        self.total_label.pack(side="left", padx=30, pady=10)

        self.count_label = tk.Label(stats, text="Number of Expenses: 0", font=("Helvetica", 12, "bold"), bg="#ecf0f1", fg="#2c3e50")
        self.count_label.pack(side="left", padx=30, pady=10)

        self.update_stats()

    def build_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(fill="x", pady=5)

        buttons = [
            ("Add Expense", self.add_expense),
            ("View Expenses", self.view_expenses),
            ("Search Expense", self.search_expense),
            ("Delete Expense", self.delete_expense),
            ("Exit", self.root.quit),
        ]

        for text, cmd in buttons:
            tk.Button(
                btn_frame,
                text=text,
                font=("Helvetica", 11),
                width=15,
                bg="#3498db",
                fg="white",
                activebackground="#2980b9",
                activeforeground="white",
                relief="flat",
                command=cmd,
            ).pack(side="left", padx=8, pady=10)

    def load_expenses(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    self.expenses = json.load(f)
        except Exception:
            self.expenses = []

    def save_expenses(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.expenses, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save expenses:\n{e}")

    def update_stats(self):
        try:
            total = sum(float(e.get("amount", 0)) for e in self.expenses)
        except Exception:
            total = 0.0
        self.total_label.config(text=f"Total Expenses: ${total:.2f}")
        self.count_label.config(text=f"Number of Expenses: {len(self.expenses)}")

    def add_expense(self):
        form = tk.Toplevel(self.root)
        form.title("Add Expense")
        form.geometry("320x300")
        form.resizable(False, False)
        form.grab_set()

        tk.Label(form, text="Date (YYYY-MM-DD):", font=("Helvetica", 10)).pack(pady=(15, 2))
        date_entry = tk.Entry(form, font=("Helvetica", 11))
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(pady=2)

        tk.Label(form, text="Category:", font=("Helvetica", 10)).pack(pady=(5, 2))
        category_var = tk.StringVar(value=CATEGORIES[0])
        ttk.Combobox(form, textvariable=category_var, values=CATEGORIES, state="readonly", font=("Helvetica", 11)).pack(pady=2)

        tk.Label(form, text="Description:", font=("Helvetica", 10)).pack(pady=(5, 2))
        desc_entry = tk.Entry(form, font=("Helvetica", 11))
        desc_entry.pack(pady=2)

        tk.Label(form, text="Amount:", font=("Helvetica", 10)).pack(pady=(5, 2))
        amount_entry = tk.Entry(form, font=("Helvetica", 11))
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

            self.expenses.append({
                "date": date,
                "category": category,
                "description": description,
                "amount": amount_val,
            })
            self.save_expenses()
            self.update_stats()
            form.destroy()
            messagebox.showinfo("Success", "Expense added successfully.")

        tk.Button(form, text="Save", font=("Helvetica", 11), bg="#27ae60", fg="white", width=12, command=save).pack(pady=15)

    def view_expenses(self):
        if not self.expenses:
            messagebox.showinfo("No Expenses", "There are no expenses to show.")
            return

        view = tk.Toplevel(self.root)
        view.title("View Expenses")
        view.geometry("620x400")
        view.grab_set()

        tree = ttk.Treeview(view, columns=("Date", "Category", "Description", "Amount"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Category", text="Category")
        tree.heading("Description", text="Description")
        tree.heading("Amount", text="Amount")
        tree.column("Date", width=110)
        tree.column("Category", width=110)
        tree.column("Description", width=250)
        tree.column("Amount", width=100)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for idx, e in enumerate(self.expenses):
            tree.insert("", "end", iid=idx, values=(e.get("date", ""), e.get("category", ""), e.get("description", ""), f"${e.get('amount', 0):.2f}"))

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
            result_win.geometry("620x400")
            result_win.grab_set()

            tree = ttk.Treeview(result_win, columns=("Date", "Category", "Description", "Amount"), show="headings")
            tree.heading("Date", text="Date")
            tree.heading("Category", text="Category")
            tree.heading("Description", text="Description")
            tree.heading("Amount", text="Amount")
            tree.column("Date", width=110)
            tree.column("Category", width=110)
            tree.column("Description", width=250)
            tree.column("Amount", width=100)
            tree.pack(fill="both", expand=True, padx=10, pady=10)

            for e in results:
                tree.insert("", "end", values=(e.get("date", ""), e.get("category", ""), e.get("description", ""), f"${e.get('amount', 0):.2f}"))

        tk.Button(search, text="Search", font=("Helvetica", 11), bg="#3498db", fg="white", width=12, command=do_search).pack(pady=15)

    def delete_expense(self):
        if not self.expenses:
            messagebox.showinfo("No Expenses", "There are no expenses to delete.")
            return

        delete_win = tk.Toplevel(self.root)
        delete_win.title("Delete Expense")
        delete_win.geometry("620x420")
        delete_win.grab_set()

        tree = ttk.Treeview(delete_win, columns=("Date", "Category", "Description", "Amount"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Category", text="Category")
        tree.heading("Description", text="Description")
        tree.heading("Amount", text="Amount")
        tree.column("Date", width=110)
        tree.column("Category", width=110)
        tree.column("Description", width=250)
        tree.column("Amount", width=100)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for idx, e in enumerate(self.expenses):
            tree.insert("", "end", iid=idx, values=(e.get("date", ""), e.get("category", ""), e.get("description", ""), f"${e.get('amount', 0):.2f}"))

        def do_delete():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select an expense to delete.")
                return

            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?")
            if not confirm:
                return

            for item in selected:
                del self.expenses[int(item)]
            self.save_expenses()
            self.update_stats()
            delete_win.destroy()
            messagebox.showinfo("Deleted", "Expense deleted successfully.")

        tk.Button(delete_win, text="Delete Selected", font=("Helvetica", 11), bg="#e74c3c", fg="white", width=15, command=do_delete).pack(pady=10)


def main():
    root = tk.Tk()
    ExpenseTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()