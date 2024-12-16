from datetime import datetime

class BillManager:
    def __init__(self):

        #Starts bill manager
        self.bills = []

    def add_bill(self, bill):
        #Add bill to list of bills
        self.bills.append(bill)
    def get_unpaid_bills(self):
        # returns a list of unpaid bills
        return [bill for bill in self.bills if not bill.is_paid]
    def sort_bills(self, by="due_date"):
        # sort bill by date or amount
        if by == "due_date":
            self.bills.sort(key=lambda bill: datetime.strptime(bill.due_date, "%Y-%m-%d"))
        elif by == "amount":
            self.bills.sort(key=lambda bill: bill.amount)
    def get_overdue_bills(self):
        # get a list of overdue bills
        return [bill for bill in self.bills if not bill.is_paid and datetime.strptime(bill.due_date,"%Y-%m-%d")]
