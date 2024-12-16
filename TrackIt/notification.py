from datetime import datetime, timedelta

class Notification:
    def __init__(self, bill_manager):
        #initalize notification
        self.bill_manager = bill_manager

    def get_overdue_notifications(self):

        #Get notifications for overdue bill
        overdue_bills = self.bill_manager.get_overdue_bills()
        notifications = [
            f"Overdue: {bill.name} (${bill.amount}) was due on {bill.due_date}!"
            for bill in overdue_bills
        ]
        return notifications

    def get_upcoming_notifications(self, days=7):
        #get notification for bill within the next 7 days
        today = datetime.now().date()
        upcoming_bills = [
            bill for bill in self.bill_manager.bills
            if not bill.is_paid and
            today <= datetime.strptime(bill.due_date, "%Y-%m-%d").date() <= today + timedelta(days=days)
        ]
        notifications = [
            f"Upcoming: {bill.name} (${bill.amount}) is due on {bill.due_date}!"
            for bill in upcoming_bills
        ]
        return notifications
