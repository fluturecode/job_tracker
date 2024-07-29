import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

# Initialize the CSV file
file_name = 'job_applications.csv'
if not os.path.isfile(file_name):
    df = pd.DataFrame(columns=['Date', 'Company', 'Position', 'Status', 'Category', 'Followed Up', 'Company Website'])
    df.to_csv(file_name, index=False)

class JobTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Tracker")
        self.style = ttk.Style(self.root)
        self.current_theme = 'light'
        self.create_widgets()
        self.load_applications()
        self.set_theme('light')

    def create_widgets(self):
        # Define the layout
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill='x', expand=True)

        self.date_label = ttk.Label(self.frame, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        self.company_label = ttk.Label(self.frame, text="Company:")
        self.company_label.grid(row=1, column=0, padx=5, pady=5)
        self.company_entry = ttk.Entry(self.frame)
        self.company_entry.grid(row=1, column=1, padx=5, pady=5)

        self.position_label = ttk.Label(self.frame, text="Position:")
        self.position_label.grid(row=2, column=0, padx=5, pady=5)
        self.position_entry = ttk.Entry(self.frame)
        self.position_entry.grid(row=2, column=1, padx=5, pady=5)

        self.status_label = ttk.Label(self.frame, text="Status:")
        self.status_label.grid(row=3, column=0, padx=5, pady=5)
        self.status_entry = ttk.Entry(self.frame)
        self.status_entry.grid(row=3, column=1, padx=5, pady=5)

        self.category_label = ttk.Label(self.frame, text="Category:")
        self.category_label.grid(row=4, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.OptionMenu(self.frame, self.category_var, "Tech", "Tech", "Blockchain", "AI")
        self.category_menu.grid(row=4, column=1, padx=5, pady=5)

        self.followup_label = ttk.Label(self.frame, text="Follow-Up Date (YYYY-MM-DD):")
        self.followup_label.grid(row=5, column=0, padx=5, pady=5)
        self.followup_entry = ttk.Entry(self.frame)
        self.followup_entry.grid(row=5, column=1, padx=5, pady=5)

        self.website_label = ttk.Label(self.frame, text="Company Website:")
        self.website_label.grid(row=6, column=0, padx=5, pady=5)
        self.website_entry = ttk.Entry(self.frame)
        self.website_entry.grid(row=6, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.frame, text="Add Application", command=self.add_application)
        self.add_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.switch_button = ttk.Button(self.frame, text="Switch to Dark Mode", command=self.toggle_theme)
        self.switch_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Date", "Company", "Position", "Status", "Category", "Followed Up", "Company Website"), show='headings')
        self.tree.heading("Date", text="Date")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Position", text="Position")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Followed Up", text="Followed Up")
        self.tree.heading("Company Website", text="Company Website")
        self.tree.pack(padx=10, pady=10, fill='x', expand=True)

    def add_application(self):
        date = self.date_entry.get()
        company = self.company_entry.get()
        position = self.position_entry.get()
        status = self.status_entry.get()
        category = self.category_var.get()
        followup = self.followup_entry.get()
        website = self.website_entry.get()

        if date and company and position and status and category and followup and website:
            new_data = pd.DataFrame([[date, company, position, status, category, followup, website]], 
                                    columns=['Date', 'Company', 'Position', 'Status', 'Category', 'Followed Up', 'Company Website'])
            new_data.to_csv(file_name, mode='a', header=False, index=False)
            self.load_applications()
            self.clear_entries()
            messagebox.showinfo("Success", "Job application added successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields")

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.category_var.set("Tech")
        self.followup_entry.delete(0, tk.END)
        self.website_entry.delete(0, tk.END)

    def load_applications(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        df = pd.read_csv(file_name)
        for index, row in df.iterrows():
            self.tree.insert("", "end", values=(row["Date"], row["Company"], row["Position"], row["Status"], row["Category"], row["Followed Up"], row["Company Website"]))

    def toggle_theme(self):
        if self.current_theme == 'light':
            self.set_theme('dark')
            self.current_theme = 'dark'
            self.switch_button.config(text="Switch to Light Mode")
        else:
            self.set_theme('light')
            self.current_theme = 'light'
            self.switch_button.config(text="Switch to Dark Mode")

    def set_theme(self, theme):
        if theme == 'light':
            self.style.configure('.', background='white', foreground='black', fieldbackground='white')
            self.style.configure('TLabel', background='white', foreground='black')
            self.style.configure('TEntry', background='white', foreground='black')
            self.style.configure('TButton', background='white', foreground='black')
            self.style.configure('TOptionMenu', background='white', foreground='black')
            self.style.configure('Treeview', background='white', foreground='black', fieldbackground='white')
            self.style.map('Treeview', background=[('selected', 'gray')], foreground=[('selected', 'white')])
        else:
            self.style.configure('.', background='black', foreground='white', fieldbackground='black')
            self.style.configure('TLabel', background='black', foreground='white')
            self.style.configure('TEntry', background='black', foreground='white')
            self.style.configure('TButton', background='black', foreground='white')
            self.style.configure('TOptionMenu', background='black', foreground='white')
            self.style.configure('Treeview', background='black', foreground='white', fieldbackground='black')
            self.style.map('Treeview', background=[('selected', 'dark gray')], foreground=[('selected', 'white')])

if __name__ == "__main__":
    root = tk.Tk()
    app = JobTrackerApp(root)
    root.mainloop()