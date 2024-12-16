#import of datetime module
from datetime import datetime

class Bill:
    #storing names to be accessed later
    def __init__(self, name, amount, due_date):
        self.name = name
        self.amount = amount
        self.due_date = due_date
        self.is_paid = False
        self.paid_date = None  # Initialize the paid_date to nothing
#marks the bills as paid
    def mark_paid(self):
        self.is_paid = True
        self.paid_date = datetime.now().strftime("%Y-%m-%d")  # Set the paid_date when the bill is paid
#will show objects as string
    def __str__(self):
        # this will show the bill as a raw string
        check = "paid" if self.is_paid else "not paid"
        return f"{self.name}: {self.amount} - Due: {self.due_date} - {check}"

