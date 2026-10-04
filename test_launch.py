import tkinter
import main

r = tkinter.Tk()
r.withdraw()
app = main.ExpenseTracker(r)
r.update_idletasks()
print("Window title:", r.title())
print("Window state:", r.state())
print("Columns:", list(app.tree.cget("columns")))
print("Expenses loaded:", len(app.expenses))
print("Tree rows:", len(app.tree.get_children()))
print("Logo:", app.logo_img.width(), "x", app.logo_img.height() if app.logo_img else "none")
print("xscroll bound:", app.tree.cget("xscrollcommand") != "")
print("yscroll bound:", app.tree.cget("yscrollcommand") != "")
r.destroy()
print("APP LAUNCHES OK")