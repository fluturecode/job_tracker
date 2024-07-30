import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# Initialize the CSV file
file_name = 'job_applications.csv'
if not os.path.isfile(file_name) or os.stat(file_name).st_size == 0:
    df = pd.DataFrame(columns=['Date', 'Company', 'Position', 'Status', 'Category', 'Followed Up', 'Company Website'])
    df.to_csv(file_name, index=False)

class JobTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Tracker")
        self.create_widgets()
        self.load_applications()

    def create_widgets(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill='x', expand=True)

        # Labels and entry fields
        self.create_label_entry(frame, "Date", DateEntry, 0)
        self.create_label_entry(frame, "Company", ttk.Entry, 1)
        self.create_label_entry(frame, "Position", ttk.Entry, 2)
        self.create_label_entry(frame, "Status", ttk.Entry, 3)

        # Category dropdown
        self.create_label_dropdown(frame, "Category", ["Tech", "Blockchain", "AI"], 4)

        # Follow-Up Date
        self.create_label_entry(frame, "Follow_Up_Date", DateEntry, 5)
        self.create_label_entry(frame, "Company_Website", ttk.Entry, 6)

        # Buttons
        self.add_button = ttk.Button(frame, text="Add Application", command=self.add_application)
        self.add_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Treeview for displaying applications
        self.tree = ttk.Treeview(self.root, columns=("Date", "Company", "Position", "Status", "Category", "Followed Up", "Company Website"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def create_label_entry(self, frame, text, widget_class, row):
        label = ttk.Label(frame, text=f"{text}:")
        label.grid(row=row, column=0, sticky='e', pady=5)
        entry = widget_class(frame)
        entry.grid(row=row, column=1, sticky='ew', pady=5)
        setattr(self, text.lower(), entry)

    def create_label_dropdown(self, frame, text, options, row):
        label = ttk.Label(frame, text=f"{text}:")
        label.grid(row=row, column=0, sticky='e', pady=5)
        var = tk.StringVar(value=options[0])
        dropdown = ttk.OptionMenu(frame, var, options[0], *options)
        dropdown.grid(row=row, column=1, sticky='ew', pady=5)
        setattr(self, text.lower(), var)

    def add_application(self):
        data = {
            "Date": self.date.get_date().strftime("%Y-%m-%d"),
            "Company": self.company.get(),
            "Position": self.position.get(),
            "Status": self.status.get(),
            "Category": self.category.get(),
            "Followed Up": self.follow_up_date.get_date().strftime("%Y-%m-%d") if self.follow_up_date.get_date() else "N/A",
            "Company Website": self.company_website.get()
        }
        if all(value for key, value in data.items() if key != "Followed Up"):
            new_data = pd.DataFrame([data])
            new_data.to_csv(file_name, mode='a', header=False, index=False)
            self.load_applications()
            self.clear_entries()
            messagebox.showinfo("Success", "Job application added successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields except Follow-Up Date")

    def clear_entries(self):
        for attr in ["company", "position", "status", "company_website"]:
            getattr(self, attr).delete(0, tk.END)
        self.date.set_date(None)
        self.category.set("Tech")
        self.follow_up_date.set_date(None)

    def load_applications(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        df = pd.read_csv(file_name)
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=tuple(row))

if __name__ == "__main__":
    root = tk.Tk()
    app = JobTrackerApp(root)
    root.mainloop()