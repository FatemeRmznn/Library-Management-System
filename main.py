import tkinter as tk
import pyodbc
from tkinter import messagebox
from PIL import Image, ImageTk
from reader_dashboard import open_reader_dashboard
from staff_dashboard import open_staff_dashboard


# Connect to my SQL Server database
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-D5JS7NNP;'
    'DATABASE=Library_Management;'
    'Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()


def login():
    username = entry_username.get()
    password = entry_password.get()

    # Check Readers table
    query_reader = "SELECT COUNT(*) FROM Readers WHERE ID_number = ? AND password_hash = ?"
    cursor.execute(query_reader, (username, password))
    result_reader = cursor.fetchone()[0]

    # Check Staffs table
    query_staff = "SELECT COUNT(*) FROM Staff WHERE ID_number = ? AND password_hash = ?"
    cursor.execute(query_staff, (username, password))
    result_staff = cursor.fetchone()[0]

    if result_reader == 1:
        role = "Reader"
        table_name = "Readers"
    elif result_staff == 1:
        role = "Staff"
        table_name = "Staff"
    else:
        messagebox.showerror("Login Error", "\tSorry! \nID_number or password was not correct. \n\tPlease try again.")
        return

    # Retrieve the user's first name from the database
    query = f"SELECT first_name FROM {table_name} WHERE ID_number = ?"
    cursor.execute(query, (username,))
    first_name = cursor.fetchone()[0]

    # Display a welcome message
    messagebox.showinfo("Login", f"Welcome to the library, {first_name} ({role})!")

    # Fetch and pass the user_id to the dashboard
    if role == "Reader":
        query = "SELECT reader_id FROM Readers WHERE ID_number = ?"
        cursor.execute(query, username)
        user_id = cursor.fetchone()[0]
        open_reader_dashboard(user_id)
    elif role == "Staff":
        query = "SELECT staff_id FROM Staff WHERE ID_number = ?"
        cursor.execute(query, username)
        user_id = cursor.fetchone()[0]
        open_staff_dashboard(user_id)


# Create the main window
window = tk.Tk()
window.title("Login")

# Set window dimensions
width = 750
height = 500

# Set window dimensions and center on screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

# Load the image and resize it
try:
    image = Image.open("library.jpg")
    resized_image = image.resize((width, height), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
except FileNotFoundError:
    messagebox.showerror("Error", "Image file 'library.jpg' not found.")
    exit()

# Create a label with the image as the background
background_label = tk.Label(window, image=bg_image)
background_label.image = bg_image  # Keep a reference!
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Configure font
font_style = ("Arial", 12)

# ID_number label and entry field
label_username = tk.Label(window, text="ID_number:", font=font_style, bg="white")
label_username.pack(pady=(50, 5))
entry_username = tk.Entry(window, font=font_style)
entry_username.pack(pady=(0, 20))

# Password label and entry field
label_password = tk.Label(window, text="Password:", font=font_style, bg="white")
label_password.pack(pady=(5, 5))
entry_password = tk.Entry(window, show="*", font=font_style)
entry_password.pack(pady=(0, 20))

# Login button
button_login = tk.Button(window, text="Login", command=login, font=font_style)
button_login.pack(pady=20)

# Run the main event loop
window.mainloop()
