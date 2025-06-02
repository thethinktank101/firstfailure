import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import backend

class SpendingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spending Habits Tracker")
        self.expenses = backend.load_data()
        self.create_widgets()
        self.update_expenses_list()

    def create_widgets(self):
        # Labels and Entry fields
        ttk.Label(self.root, text="Date (MM/DD/YYYY):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%m/%d/%Y"))

        ttk.Label(self.root, text="Amount ($):").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Category:").grid(row=2, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.root)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Description:").grid(row=3, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(self.root)
        self.desc_entry.grid(row=3, column=1, padx=5, pady=5)

        # Listbox for expenses
        self.expenses_listbox = tk.Listbox(self.root, width=60, height=10)
        self.expenses_listbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        self.expenses_listbox.bind('<<ListboxSelect>>', self.load_selected_expense)

        # Buttons
        ttk.Button(self.root, text="Add Expense", command=self.add_expense).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(self.root, text="View Expenses", command=self.view_expenses).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Show Summary", command=self.show_summary).grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(self.root, text="Update Expense", command=self.update_expense).grid(row=8, column=0, pady=5)
        ttk.Button(self.root, text="Delete Expense", command=self.delete_expense).grid(row=8, column=1, pady=5)


        # Output textbox
        self.output = tk.Text(self.root, width=60, height=15)
        self.output.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def update_expenses_list(self):
        self.expenses_listbox.delete(0, tk.END)
        for idx, e in enumerate(self.expenses):
            line = (f"{idx+1}. Date: {e['date']}, Amount: ${e['amount']:.2f}, "
                    f"Category: {e['category']}, Description: {e['description']}")
            self.expenses_listbox.insert(tk.END, line)

    def add_expense(self):
        date = self.date_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for amount.")
            return
        category = self.category_entry.get()
        description = self.desc_entry.get()

        expense = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        backend.add_expense(self.expenses, expense)
        backend.save_data(self.expenses)
        self.update_expenses_list()
        messagebox.showinfo("Success", "Expense added!")
        self.clear_entries()

    def update_expense(self):
        if not hasattr(self, 'edit_index'):
            messagebox.showerror("Error", "Please select an expense to update.")
            return
        index = self.edit_index
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for amount.")
            return
        updated_expense = {
            "date": self.date_entry.get(),
            "amount": amount,
            "category": self.category_entry.get(),
            "description": self.desc_entry.get()
        }
        self.expenses

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%m/%d/%Y"))

    def load_selected_expense(self, event):
        selection = self.expenses_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.edit_index = index  # Save index for reference
        expense = self.expenses[index]
        # Fill entries with selected expense data
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, expense['date'])
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(expense['amount']))
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, expense['category'])
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, expense['description'])

    def delete_expense(self):
        if not hasattr(self, 'edit_index'):
            messagebox.showerror("Error", "Please select an expense to delete.")
            return
        index = self.edit_index
        del self.expenses[index]
        backend.save_data(self.expenses)
        self.update_expenses_list()
        # Clear input fields
        self.clear_entries()
        # Remove the selection reference
        del self.edit_index
        messagebox.showinfo("Deleted", "Expense has been deleted.")
    
    def view_expenses(self):
        self.output.delete('1.0', tk.END)
        if not self.expenses:
            self.output.insert(tk.END, "No expenses recorded.\n")
            return
        for idx, e in enumerate(self.expenses, 1):
            line = f"{idx}. Date: {e['date']}, Amount: ${e['amount']:.2f}, Category: {e['category']}, Description: {e['description']}\n"
            self.output.insert(tk.END, line)


    def show_summary(self):
        self.output.delete('1.0', tk.END)
        total, category_totals = backend.get_summary(self.expenses)
        self.output.insert(tk.END, f"Total spending: ${total:.2f}\n")
        self.output.insert(tk.END, "Spending by category:\n")
        for cat, amt in category_totals.items():
            self.output.insert(tk.END, f"  {cat}: ${amt:.2f}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpendingApp(root)
    root.mainloop()
