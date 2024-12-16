"""
This application is a finace app for my final project
in SDEV 220 the application is a bill tracking and management app
finacial advisor can give program to user to run locally on their machine
users can add bills with details and be reminded of them
Daniel Anderson
Version 1
SDEV220
Module 8 Final Project
"""
import tkinter as tk # used for GUI
from tkinter import messagebox #to show box warnings
from bill import Bill #importing the Bill class from bill.py
from bill_manager import BillManager #used for collections of fills
from notification import Notification # used for notifications of bills
import os # used to navigate to file path for logo.
from datetime import datetime # used to work with dates

# Creation of the main window for the application
class BillTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trackit")
        self.root.geometry("600x400")

# Initialize BillManager and Notification
        self.manager = BillManager()
        self.notifier = Notification(self.manager)

# interface setup call to create buttons visuals
        self.create_widgets()
    def create_widgets(self):
        # getting logo image, positioning image and error handling
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "TrackIt.png")
            self.logo = tk.PhotoImage(file=logo_path)
            self.logo_label = tk.Label(self.root, image=self.logo)
            self.logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Bill List section
        self.bill_list_label = tk.Label(self.root, text="Bill List", font=("Helvetica", 16))# label for bill section
        self.bill_list_label.pack(pady=10)

        self.bill_listbox = tk.Listbox(self.root, width=50, height=10) # creation of box for the list of bills
        self.bill_listbox.pack(pady=10)

        # creations of buttons below
        # Update the bill section with the current bills
        self.update_bill_list()

        # Add Bill Button
        self.add_bill_button = tk.Button(self.root, text="Add Bill", command=self.add_bill)
        self.add_bill_button.pack(pady=5)

        # Mark Bill Paid Button
        self.mark_paid_button = tk.Button(self.root, text="Mark Bill Paid", command=self.mark_bill_paid)
        self.mark_paid_button.pack(pady=5)

        # View Overdue Notifications Button
        self.view_overdue_button = tk.Button(self.root, text="View Overdue Notifications",
                                             command=self.view_overdue_notifications)
        self.view_overdue_button.pack(pady=5)

        # View Upcoming Notifications Button
        self.view_upcoming_button = tk.Button(self.root, text="View Upcoming Notifications",
                                              command=self.view_upcoming_notifications)
        self.view_upcoming_button.pack(pady=5)

        # Sorting Button (Sort by Amount)
        self.sort_amount_button = tk.Button(self.root, text="Sort by Amount", command=self.sort_by_amount)
        self.sort_amount_button.pack(pady=5)

        # Sorting Button (Sort by Due Date)
        self.sort_due_date_button = tk.Button(self.root, text="Sort by Due Date", command=self.sort_by_due_date)
        self.sort_due_date_button.pack(pady=5)

        # View Paid Bills Button
        self.view_paid_button = tk.Button(self.root, text="View Paid Bills", command=self.view_paid_bills)
        self.view_paid_button.pack(pady=5)

        # Footer label at the bottom of page
        self.footer_label = tk.Label(self.root, text="TrackIt Bill Tracker - Your Personal Finance Assistant",
                                     font=("Helvetica", 8), fg="gray")
        self.footer_label.pack(side=tk.BOTTOM, pady=10)

    def update_bill_list(self):
        # clearing the bills to update
        self.bill_listbox.delete(0, tk.END)  # Clear existing list
        for bill in self.manager.get_unpaid_bills():
            bill_info = f"{bill.name}: ${bill.amount} - Due: {bill.due_date} - Status: {'Paid' if bill.is_paid else 'Unpaid'}"
            self.bill_listbox.insert(tk.END, bill_info)

    def add_bill(self):
        #method for adding new bill
        def submit_bill():
            name = name_entry.get()
            amount_str = amount_entry.get()
            due_date = due_date_entry.get()

            # error handling
            if not name or not amount_str or not due_date:
                messagebox.showwarning("Input Error", "All fields must be filled out!")
                return


            try:
                amount = float(amount_str)
            except ValueError:
                messagebox.showwarning("Input Error", "Amount must be a valid number!")
                return


            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Input Error", "Due date must be in the format YYYY-MM-DD!")
                return

            # If bill pass checks bills will be added
            self.manager.add_bill(Bill(name, amount, due_date))
            self.update_bill_list()
            add_bill_window.destroy()

        add_bill_window = tk.Toplevel(self.root)
        add_bill_window.title("Add New Bill")

        tk.Label(add_bill_window, text="Enter Bill Details", font=("Helvetica", 14)).pack(pady=5)

        tk.Label(add_bill_window, text="Bill Name").pack(pady=5)
        name_entry = tk.Entry(add_bill_window)
        name_entry.pack(pady=5)

        tk.Label(add_bill_window, text="Amount ($)").pack(pady=5)
        amount_entry = tk.Entry(add_bill_window)
        amount_entry.pack(pady=5)

        tk.Label(add_bill_window, text="Due Date (YYYY-MM-DD)").pack(pady=5)
        due_date_entry = tk.Entry(add_bill_window)
        due_date_entry.pack(pady=5)

        submit_button = tk.Button(add_bill_window, text="Submit", command=submit_bill)
        submit_button.pack(pady=10)

    def mark_bill_paid(self):
        #if bill is selected with mouse and marked as paid if no bill selected will get message
        selected_bill = self.bill_listbox.curselection()
        if selected_bill:
            bill_index = selected_bill[0]
            bill = self.manager.get_unpaid_bills()[bill_index]
            bill.mark_paid()
            self.update_bill_list()
        else:
            messagebox.showwarning("No Selection", "Please select a bill to mark as paid.")

    def view_overdue_notifications(self):
        #shows upcoming bills if no bills shows no bills
        overdue_notifications = self.notifier.get_overdue_notifications()
        if overdue_notifications:
            messagebox.showinfo("Overdue Bills", "\n".join(overdue_notifications))
        else:
            messagebox.showinfo("No Overdue Bills", "No overdue bills at the moment.")

    def view_upcoming_notifications(self):
        upcoming_notifications = self.notifier.get_upcoming_notifications()
        if upcoming_notifications:
            messagebox.showinfo("Upcoming Bills", "\n".join(upcoming_notifications))
        else:
            messagebox.showinfo("No Upcoming Bills", "No upcoming bills in the next few days.")

        # sorting bills by amount and date
    def sort_by_amount(self):
        self.manager.sort_bills(by="amount")
        self.update_bill_list()

    def sort_by_due_date(self):
        self.manager.sort_bills(by="due_date")
        self.update_bill_list()

        # creation of window with bills that have been paid
    def view_paid_bills(self):
        paid_bills_window = tk.Toplevel(self.root)
        paid_bills_window.title("Paid Bills")

        paid_bills_listbox = tk.Listbox(paid_bills_window, width=50, height=10)
        paid_bills_listbox.pack(pady=10)

        # Get paid bills and display them
        paid_bills = [bill for bill in self.manager.bills if bill.is_paid]
        if paid_bills:
            for bill in paid_bills:
                paid_bills_listbox.insert(tk.END, f"{bill.name}: ${bill.amount} - Paid on: {bill.paid_date}")
        else:
            paid_bills_listbox.insert(tk.END, "No bills have been paid yet.")


# main window
root = tk.Tk()
app = BillTrackerApp(root)
root.mainloop()
