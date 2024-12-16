import tkinter as tk
from interface import BillTrackerApp

def main():
    #main window
    root = tk.Tk()
    app = BillTrackerApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()
