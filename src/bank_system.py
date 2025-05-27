import csv
import re
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

class BankSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Loan Management System")
        
        
        self.root.state('normal')
        root.resizable(False, False)
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('TLabel', font=('Helvetica', 10))
        
        # Create main container
        self.container = ttk.Frame(root)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Initialize frames
        self.frames = {}
        for F in (MainPage, DatabasePage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainPage)
        
        # Initialize database file
        self.initialize_database()
        
    def initialize_database(self):
        """Ensure the database file exists with correct headers"""
        try:
            with open("database.csv", "r") as file:
                # Check if file has headers
                reader = csv.reader(file)
                headers = next(reader, None)
                required_headers = [
                    "Name", "Email", "Date of Birth", "Loan amount",
                    "Interest amount", "Interest money", "Month",
                    "Interest money per month"
                ]
                
                if headers != required_headers:
                    # File exists but has wrong headers - recreate it
                    raise ValueError("Incorrect headers in database file")
                    
        except (FileNotFoundError, ValueError):
            # Create new file with correct headers
            with open("database.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "Name", "Email", "Date of Birth", 
                    "Loan amount", "Interest amount", 
                    "Interest money", "Month", "Interest money per month"
                ])
                writer.writeheader()
        except Exception as e:
            messagebox.showerror("Initialization Error", 
                               f"Failed to initialize database:\n{str(e)}")
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if cont == DatabasePage:
            frame.load_data()
        
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_dob(self, dob):
        c_date = re.search(r"^(\d{4})-(0[1-9]|1[0-2])-([0-2][0-9]|3[01])$", dob)
        return c_date and c_date.group(0) < "2025"
    
    def calculate_interest(self, amount, rate):
        return int(amount / 100 * rate)
    
    def calculate_monthly_interest(self, interest_amount, months):
        return interest_amount * months
    
    def load_database(self):
        try:
            with open("database.csv", "r") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as e:
            messagebox.showerror("Database Error", 
                               f"An error occurred while accessing the database:\n{str(e)}")
            return None
    
    def email_exists(self, email):
        """Check if email already exists in database"""
        records = self.load_database()
        if records is None:
            return False
        return any(record['Email'].lower() == email.lower() for record in records)

class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Configure grid weights for centering
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        # Main content frame (centered)
        main_frame = ttk.Frame(self)
        main_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        # Header
        header = ttk.Label(main_frame, text="Loan Application Form", style='Header.TLabel')
        header.pack(pady=20)
        
        # Form Frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Configure form grid
        for i in range(6):
            form_frame.grid_rowconfigure(i, weight=1)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Customer Name
        ttk.Label(form_frame, text="Customer Full Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=40)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Email
        ttk.Label(form_frame, text="Email Address:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(form_frame, width=40)
        self.email_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Date of Birth
        ttk.Label(form_frame, text="Date of Birth (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.dob_entry = ttk.Entry(form_frame, width=40)
        self.dob_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Loan Amount
        ttk.Label(form_frame, text="Loan Amount ($):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.loan_entry = ttk.Entry(form_frame, width=40)
        self.loan_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Interest Rate
        ttk.Label(form_frame, text="Interest Rate (%):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.interest_entry = ttk.Entry(form_frame, width=40)
        self.interest_entry.grid(row=4, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Months
        ttk.Label(form_frame, text="Loan Term (Months):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.month_entry = ttk.Entry(form_frame, width=40)
        self.month_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Calculation Results", padding=10)
        results_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.loan_result = ttk.Label(results_frame, text="")
        self.loan_result.pack(anchor=tk.W)
        
        self.interest_result = ttk.Label(results_frame, text="")
        self.interest_result.pack(anchor=tk.W)
        
        self.month_result = ttk.Label(results_frame, text="")
        self.month_result.pack(anchor=tk.W)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20)
        
        ttk.Button(buttons_frame, text="Submit Application", 
                  command=self.submit_data).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(buttons_frame, text="View Database", 
                  command=lambda: self.controller.show_frame(DatabasePage)).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(buttons_frame, text="Clear Form", 
                  command=self.clear_fields).pack(side=tk.LEFT, padx=10)
    
    def submit_data(self):
        # Get all values
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        dob = self.dob_entry.get().strip()
        loan_amount = self.loan_entry.get().strip()
        interest_rate = self.interest_entry.get().strip()
        months = self.month_entry.get().strip()
        
        # Validate fields
        if not name:
            messagebox.showwarning("Validation Error", "Please enter the customer's full name.")
            return
        
        if not email:
            messagebox.showwarning("Validation Error", "Please enter the customer's email address.")
            return
        
        if not self.controller.validate_email(email):
            messagebox.showwarning("Validation Error", "Please enter a valid email address (e.g., user@example.com).")
            return
            
        # Check if email already exists
        if self.controller.email_exists(email):
            messagebox.showwarning("Duplicate Email", "This email address is already registered in our system.")
            return
        
        if not dob:
            messagebox.showwarning("Validation Error", "Please enter the date of birth.")
            return
        
        if not self.controller.validate_dob(dob):
            messagebox.showwarning("Validation Error", "Please enter a valid date of birth in YYYY-MM-DD format (must be before 2025).")
            return
        
        if not loan_amount:
            messagebox.showwarning("Validation Error", "Please enter the loan amount.")
            return
        
        if not loan_amount.isdigit() or int(loan_amount) <= 0:
            messagebox.showwarning("Validation Error", "Loan amount must be a positive number.")
            return
        
        if not interest_rate:
            messagebox.showwarning("Validation Error", "Please enter the interest rate.")
            return
        
        if not interest_rate.isdigit() or int(interest_rate) <= 0:
            messagebox.showwarning("Validation Error", "Interest rate must be a positive number.")
            return
        
        if not months:
            messagebox.showwarning("Validation Error", "Please enter the loan term in months.")
            return
        
        if not months.isdigit() or int(months) <= 0:
            messagebox.showwarning("Validation Error", "Loan term must be a positive number of months.")
            return
        
        # Convert to numbers
        loan_amount_int = int(loan_amount)
        interest_rate_int = int(interest_rate)
        months_int = int(months)
        
        # Calculate results
        interest_money = self.controller.calculate_interest(loan_amount_int, interest_rate_int)
        monthly_interest = self.controller.calculate_monthly_interest(interest_money, months_int)
        
        # Update results display
        self.loan_result.config(text=f"Loan Amount: {loan_amount_int:,} $")
        self.interest_result.config(text=f"Interest Amount: {interest_rate_int}%")
        self.month_result.config(text=f"Total Interest for {months_int} months: {monthly_interest:,} $")
        
        # Prepare data for CSV
        data = {
            "Name": name.title(),
            "Email": email.lower(),
            "Date of Birth": dob,
            "Loan amount": f"{loan_amount_int} $",
            "Interest amount": f"{interest_rate_int} %",
            "Interest money": f"{interest_money} $",
            "Month": f"{months_int} months",
            "Interest money per month": f"{monthly_interest} $"
        }
        
        # Write to CSV
        try:
            with open("database.csv", "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())
                if file.tell() == 0:  # Write header if file is empty
                    writer.writeheader()
                writer.writerow(data)
            messagebox.showinfo("Application Submitted", "The loan application has been successfully submitted to our database.")
            
            # Clear form after successful submission
            self.clear_fields()
            
        except Exception as e:
            messagebox.showerror("Submission Error", f"An error occurred while saving the application:\n{str(e)}")
    
    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.loan_entry.delete(0, tk.END)
        self.interest_entry.delete(0, tk.END)
        self.month_entry.delete(0, tk.END)
        self.loan_result.config(text="")
        self.interest_result.config(text="")
        self.month_result.config(text="")

class DatabasePage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Configure grid weights for centering
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        # Main content frame (centered)
        main_frame = ttk.Frame(self)
        main_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        # Header
        header = ttk.Label(main_frame, text="Customer Database", style='Header.TLabel')
        header.pack(pady=20)
        
        # Treeview Frame
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Create Treeview with optimized column widths
        self.tree = ttk.Treeview(tree_frame, columns=(
            "Name", "Email", "Date of Birth", "Loan Amount", 
            "Interest Rate", "Interest", "Term", "Total Interest"
        ), show="headings")
        
        # Configure columns with perfect widths
        self.tree.heading("Name", text="Name")
        self.tree.column("Name", width=110, anchor=tk.W) 
        
        self.tree.heading("Email", text="Email")
        self.tree.column("Email", width=120, anchor=tk.W)  
        
        self.tree.heading("Date of Birth", text="Date of Birth")
        self.tree.column("Date of Birth", width=130, anchor=tk.W)  
        
        self.tree.heading("Loan Amount", text="Loan Amount ($)")
        self.tree.column("Loan Amount", width=140, anchor=tk.W)  
        
        self.tree.heading("Interest Rate", text="Interest Rate (%)")
        self.tree.column("Interest Rate", width=140, anchor=tk.W) 
        
        self.tree.heading("Interest", text="Monthly Interest ($)")
        self.tree.column("Interest", width=160, anchor=tk.W) 
        
        self.tree.heading("Term", text="Term (Months)")
        self.tree.column("Term", width=130, anchor=tk.W)  
        
        self.tree.heading("Total Interest", text="Total Interest ($)")
        self.tree.column("Total Interest", width=140, anchor=tk.W) 
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Use grid for better layout control
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Delete Frame
        delete_frame = ttk.Frame(main_frame)
        delete_frame.pack(pady=10)
        
        ttk.Label(delete_frame, text="Enter Email to Delete:").pack(side=tk.LEFT, padx=5)
        self.delete_entry = ttk.Entry(delete_frame, width=30)
        self.delete_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(delete_frame, text="Delete Record", 
                 command=self.delete_record).pack(side=tk.LEFT, padx=5)
        
        # Back Button
        ttk.Button(main_frame, text="Back to Application Form", 
                 command=lambda: controller.show_frame(MainPage)).pack(pady=10)
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        records = self.controller.load_database()
        if records is None:
            return
        
        for record in records:
            try:
                self.tree.insert("", tk.END, values=(
                    record.get("Name", ""),
                    record.get("Email", ""),
                    record.get("Date of Birth", ""),
                    record.get("Loan amount", ""),
                    record.get("Interest amount", ""),
                    record.get("Interest money", ""),
                    record.get("Month", ""),
                    record.get("Interest money per month", "")
                ))
            except Exception as e:
                continue
    
    def delete_record(self):
        email = self.delete_entry.get().strip()
        if not email:
            messagebox.showwarning("Input Required", "Please enter the email address of the record you wish to delete.")
            return
        
        if not self.controller.validate_email(email):
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the record for {email}?"):
            return
        
        # Read all records
        records = self.controller.load_database()
        if records is None:
            return
        
        # Filter out the record to delete
        original_count = len(records)
        new_records = [r for r in records if r["Email"].strip().lower() != email.lower()]
        
        if len(new_records) == original_count:
            messagebox.showinfo("Not Found", f"No record found with email: {email}")
            return
        
        # Write remaining records back
        try:
            with open("database.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(new_records)
            
            messagebox.showinfo("Deletion Successful", "The record has been successfully removed from the database.")
            self.load_data()  # Refresh the view
            self.delete_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Deletion Error", f"An error occurred while deleting the record:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankSystemGUI(root)
    root.mainloop()