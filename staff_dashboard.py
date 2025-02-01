import tkinter as tk
import pyodbc
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime, timedelta

# --- Database Connection ---
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-D5JS7NNP;'
    'DATABASE=Library_Management;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()


# --- UI Helper Functions ---
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def load_background(window, image_path):
    image = Image.open(image_path)
    resized_image = image.resize((900, 600), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    window.bg_image = bg_image  # Prevent garbage collection
    bg_label = tk.Label(window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


def create_label(window, text, **kwargs):
    return tk.Label(window, text=text, font=("Arial", 12), bg="white", **kwargs)


def create_entry(window, **kwargs):
    return tk.Entry(window, font=("Arial", 12), **kwargs)


def create_button(window, text, command, **kwargs):
    return tk.Button(window, text=text, command=command, font=("Arial", 12, "bold"), **kwargs)


def create_treeview(window, columns, headings):
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 11))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    tree = ttk.Treeview(window, columns=columns, show="headings")
    for col, heading in zip(columns, headings):
        tree.heading(col, text=heading)
        tree.column(col, width=120)
    return tree


def close_all_tables():
    for table in [book_table, report_table, user_table]:
        table.pack_forget()


def open_staff_dashboard(staff_id):
    global book_table, report_table, user_table  # ⬅ متغیرهای سراسری برای جداول

    dashboard = tk.Toplevel()
    dashboard.title("Staff Dashboard")
    dashboard.geometry("900x600")
    center_window(dashboard, 900, 600)
    load_background(dashboard, "library.jpg")

    book_table = create_treeview(dashboard,
                                 ["book_id", "title", "author", "publisher_id", "publication_year", "available",
                                  "category", "details"],
                                 ["Book ID", "Title", "Author", "Publisher", "Year", "Available", "Category",
                                  "Details"])

    report_table = create_treeview(dashboard,
                                   ["report_id", "reader_id", "staff_id", "action_type", "detail", "created_date"],
                                   ["Report ID", "Reader ID", "Staff ID", "Action Type", "Details", "Date"])

    user_table = create_treeview(dashboard,
                                 ["reader_id", "first_name", "last_name", "ID_number", "phone_number", "address"],
                                 ["Reader ID", "First Name", "Last Name", "ID Number", "Phone Number", "Address"])

    def close_all_tables():
        for table in [book_table, report_table, user_table]:
            table.pack_forget()

    def logout():
        dashboard.destroy()

    def open_books():
        close_all_tables()
        cursor.execute("SELECT * FROM Books")
        rows = cursor.fetchall()
        book_table.delete(*book_table.get_children())
        for row in rows:
            book_table.insert("", "end", values=[str(item) if item is not None else "" for item in row])
        book_table.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def add_book():
        add_window = tk.Toplevel()
        add_window.title("Add New Book")
        add_window.geometry("500x400")
        center_window(add_window, 500, 400)
        load_background(add_window, "library.jpg")

        labels = ["Title", "Author", "Publisher ID", "Year", "Available", "Category", "Details"]
        entries = {}
        for i, label in enumerate(labels):
            create_label(add_window, label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entries[label] = create_entry(add_window)
            entries[label].grid(row=i, column=1, padx=10, pady=5)

        def submit_book():
            values = [entries[label].get() for label in labels]
            cursor.execute(
                "INSERT INTO Books (title, author, publisher_id, publication_year, available, category, details)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                values)
            conn.commit()
            messagebox.showinfo("Success", "Book added successfully")
            add_window.destroy()

        create_button(add_window, "Submit", submit_book).grid(row=len(labels), column=1, pady=10)

    def add_report():
        add_window = tk.Toplevel()
        add_window.title("Add New Report")
        add_window.geometry("500x400")
        center_window(add_window, 500, 400)
        load_background(add_window, "library.jpg")

        labels = ["Reader ID", "Book ID", "Action Type (borrow/return)", "Details"]
        entries = {}
        for i, label in enumerate(labels):
            create_label(add_window, label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entries[label] = create_entry(add_window)
            entries[label].grid(row=i, column=1, padx=10, pady=5)

        def submit_report():
            values = [entries[label].get() for label in labels]
            cursor.execute(
                "INSERT INTO Reports (reader_id, staff_id, action_type, detail, created_date)"
                " VALUES (?, ?, ?, ?, ?)",
                (values[0], staff_id, values[1], values[2], datetime.now().strftime('%Y-%m-%d')))
            conn.commit()
            messagebox.showinfo("Success", "Report added successfully")
            add_window.destroy()

        create_button(add_window, "Submit", submit_report).grid(row=len(labels), column=1, pady=10)

    def open_reports():
        close_all_tables()
        cursor.execute("SELECT * FROM Reports")
        rows = cursor.fetchall()
        report_table.delete(*report_table.get_children())
        for row in rows:
            report_table.insert("", "end", values=[str(item) if item is not None else "" for item in row])
        report_table.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def open_users():
        close_all_tables()
        cursor.execute("SELECT * FROM Readers")
        rows = cursor.fetchall()
        user_table.delete(*user_table.get_children())
        for row in rows:
            user_table.insert("", "end", values=[str(item) if item is not None else "" for item in row])
        user_table.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def add_user():
        add_window = tk.Toplevel()
        add_window.title("Add New User")
        add_window.geometry("500x400")
        center_window(add_window, 500, 400)
        load_background(add_window, "library.jpg")

        labels = ["First Name", "Last Name", "ID Number", "Phone Number", "Address"]
        entries = {}
        for i, label in enumerate(labels):
            create_label(add_window, label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entries[label] = create_entry(add_window)
            entries[label].grid(row=i, column=1, padx=10, pady=5)

        def submit_user():
            values = [entries[label].get() for label in labels]
            cursor.execute(
                "INSERT INTO Readers (first_name, last_name, ID_number, phone_number, address)"
                " VALUES (?, ?, ?, ?, ?)",
                values)
            conn.commit()
            messagebox.showinfo("Success", "User added successfully")
            add_window.destroy()

        create_button(add_window, "Submit", submit_user).grid(row=len(labels), column=1, pady=10)

    button_frame = tk.Frame(dashboard, bg="white")
    button_frame.pack(pady=20)
    create_button(button_frame, "View Books", open_books).grid(row=0, column=0, padx=5, pady=5)
    create_button(button_frame, "Add Book", add_book).grid(row=0, column=1, padx=5, pady=5)
    create_button(button_frame, "View Reports", open_reports).grid(row=0, column=2, padx=5, pady=5)
    create_button(button_frame, "Add Report", add_report).grid(row=0, column=3, padx=5, pady=5)  # تغییر column

    create_button(button_frame, "View Users", open_users).grid(row=1, column=0, padx=5, pady=5)
    create_button(button_frame, "Add User", add_user).grid(row=1, column=1, padx=5, pady=5)
    create_button(button_frame, "Close Tables", close_all_tables).grid(row=1, column=2, padx=5, pady=5)
    create_button(button_frame, "Logout", logout).grid(row=1, column=3, padx=5, pady=5)

    dashboard.mainloop()


# Example Usage
if __name__ == "__main__":
    open_staff_dashboard(6789012345)  # Replace 101 with a valid staff_id
