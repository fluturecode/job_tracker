import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

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

        self.create_label_entry(frame, "Date", DateEntry, 0)
        self.create_label_entry(frame, "Company", ttk.Entry, 1)
        self.create_label_entry(frame, "Position", ttk.Entry, 2)
        self.create_label_entry(frame, "Status", ttk.Entry, 3)
        self.create_label_dropdown(frame, "Category", ["Tech", "Blockchain", "AI"], 4)
        self.create_label_entry(frame, "Follow_Up_Date", DateEntry, 5)
        self.create_label_entry(frame, "Company_Website", ttk.Entry, 6)

        self.add_button = ttk.Button(frame, text="Add Application", command=self.add_application)
        self.add_button.grid(row=7, column=0, columnspan=2, pady=10)

        columns = ("Date", "Company", "Position", "Status", "Category", "Followed Up", "Company Website", "Edit", "Delete")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            if col in ["Edit", "Delete"]:
                self.tree.column(col, width=50, anchor='center')
            else:
                self.tree.column(col, width=100)
        
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

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
        data = self.get_form_data()
        if all(value for key, value in data.items() if key != "Followed Up"):
            new_data = pd.DataFrame([data])
            new_data.to_csv(file_name, mode='a', header=False, index=False)
            self.load_applications()
            self.clear_entries()
            messagebox.showinfo("Success", "Job application added successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields except Follow-Up Date")

    def edit_application(self, item):
        item_values = self.tree.item(item)['values']
        self.populate_form(item_values[:-2])  # Exclude the edit and delete icons
        self.add_button.config(text="Update Application", command=lambda: self.update_application(item))

    def update_application(self, item):
        data = self.get_form_data()
        if all(value for key, value in data.items() if key != "Followed Up"):
            df = pd.read_csv(file_name)
            index = self.tree.index(item)
            df.iloc[index] = list(data.values())
            df.to_csv(file_name, index=False)
            self.load_applications()
            self.clear_entries()
            self.add_button.config(text="Add Application", command=self.add_application)
            messagebox.showinfo("Success", "Job application updated successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields except Follow-Up Date")

    def delete_application(self, item):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this application?"):
            df = pd.read_csv(file_name)
            index = self.tree.index(item)
            df = df.drop(df.index[index])
            df.to_csv(file_name, index=False)
            self.load_applications()
            messagebox.showinfo("Success", "Job application deleted successfully!")

    def get_form_data(self):
        return {
            "Date": self.date.get_date().strftime("%Y-%m-%d"),
            "Company": self.company.get(),
            "Position": self.position.get(),
            "Status": self.status.get(),
            "Category": self.category.get(),
            "Followed Up": self.follow_up_date.get_date().strftime("%Y-%m-%d") if self.follow_up_date.get_date() else "N/A",
            "Company Website": self.company_website.get()
        }
    
    def populate_form(self, values):
        # Convert the date string to a datetime object
        date_obj = datetime.strptime(values[0], "%Y-%m-%d").date()
        self.date.set_date(date_obj)
        
        self.company.delete(0, tk.END)
        self.company.insert(0, values[1])
        self.position.delete(0, tk.END)
        self.position.insert(0, values[2])
        self.status.delete(0, tk.END)
        self.status.insert(0, values[3])
        self.category.set(values[4])
        
        # Handle the Follow Up Date
        if values[5] != "N/A":
            follow_up_date_obj = datetime.strptime(values[5], "%Y-%m-%d").date()
            self.follow_up_date.set_date(follow_up_date_obj)
        else:
            self.follow_up_date.set_date(None)
        
        self.company_website.delete(0, tk.END)
        self.company_website.insert(0, values[6])

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
            values = list(row) + ["✏️", "🗑️"]  # Unicode icons for edit and delete
            self.tree.insert("", "end", values=values)

    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            column_index = int(column[1:]) - 1
            if column_index == len(self.tree["columns"]) - 2:  # Edit column
                self.edit_application(item)
            elif column_index == len(self.tree["columns"]) - 1:  # Delete column
                self.delete_application(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = JobTrackerApp(root)
    root.mainloop()