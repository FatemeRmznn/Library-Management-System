import tkinter as tk
import pyodbc
from tkinter import messagebox
from reader_dashboard import open_Reader_dashboard
from sttaf_dashboard import open_Staff_dashboard

# Connect to my SQL Server database
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-D5JS7NNP;'
    'DATABASE=Final_project;'
    'Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()
signup_option_var = None


def login():
    username = entry_username.get()
    password = entry_password.get()
    role = option_var.get()
    # validate the username and password and handle the selected role
    query = f"SELECT COUNT(*) FROM {role} WHERE ID_number = ? AND [password] = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result[0] == 1:
        # Retrieve the user's first name from the database
        query = f"SELECT first_name FROM {role} WHERE ID_number = ?"
        cursor.execute(query, (username ))
        first_name = cursor.fetchone()[0]
        # Display a welcome message
        messagebox.showinfo("Login", f"Welcome to the library, {first_name}!")
        if role == "Readers":
            query = f"SELECT reader_id FROM Readers WHERE ID_number = ?"
            cursor.execute(query, (username))
            Reader_ID = cursor.fetchone()[0]
            open_Reader_dashboard(Reader_ID)

        elif role == "Staffs":
            query = f"SELECT staff_id FROM Staffs WHERE ID_number = ?"
            cursor.execute(query, (username,))
            Staff_ID = cursor.fetchone()[0]
            open_Staff_dashboard(Staff_ID)
    else:
        # Display an error message
        messagebox.showerror("Login Error", "\tSorry! \nID_number or password was not correct. \n\tPlease try again.")


def signup():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    username = entry_username.get()
    password = entry_password.get()
    role = signup_option_var.get()

    # Check if the username already exists
    query = f"SELECT COUNT(*) FROM {role} WHERE ID_number = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result[0] > 0:
        messagebox.showerror("Sign Up Error", "ID_number already exists. Please choose a different ID_number.")
        return

    # Perform sign-up logic here
    query = f"INSERT INTO {role} (first_name, last_name, ID_number, [password]) " \
            f"VALUES (?, ?, ?, ?)"
    cursor.execute(query, (first_name, last_name, username, password))
    conn.commit()

    # Display a message box with sign-up confirmation
    messagebox.showinfo("Sign Up", "Sign-up successful!")

    # Close the database connection
    conn.close()


def open_signup_window():
    # Create a new window for the sign-up form
    signup_window = tk.Toplevel()
    signup_window.title("Sign Up")

    # Load the image
    bc_image = tk.PhotoImage(file="main.png")

    # Get the width and height of the image
    bc_image_width = bc_image.width()
    bc_image_height = bc_image.height()

    # Set the maximum width for resizing
    bc_max_width = 700

    # Calculate the appropriate window height to maintain image aspect ratio within the maximum width
    bc_window_height = int(bc_image_height * bc_max_width / bc_image_width)

    # Set the minimum and maximum window sizes
    signup_window.minsize(400, 400)  # Replace with your desired minimum size
    signup_window.maxsize(bc_max_width, bc_window_height)

    # Create a label with the image as the background
    background_signup_label = tk.Label(signup_window, image=bc_image)
    background_signup_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ID_number label and entry field
    label_username = tk.Label(signup_window, text="ID_number:")
    label_username.pack()
    global entry_username
    entry_username = tk.Entry(signup_window)
    entry_username.pack(pady=(0, 10))

    # Password label and entry field
    label_password = tk.Label(signup_window, text="Password:")
    label_password.pack()
    global entry_password  # Declare as global
    entry_password = tk.Entry(signup_window, show="*")
    entry_password.pack()

    # First name
    label_first_name = tk.Label(signup_window, text="First Name:")
    label_first_name.pack()
    global entry_first_name  # Declare as global
    entry_first_name = tk.Entry(signup_window)
    entry_first_name.pack()

    # Last Name
    label_last_name = tk.Label(signup_window, text="Last Name:")
    label_last_name.pack()
    global entry_last_name  # Declare as global
    entry_last_name = tk.Entry(signup_window)
    entry_last_name.pack()

    # Option box for sign-up
    global signup_option_var  # Declare as global
    signup_option_var = tk.StringVar()
    signup_option_var.set("Readers")  # Set a default option

    signup_option_box = tk.OptionMenu(signup_window, signup_option_var, "Staffs", "Readers")
    signup_option_box.pack()

    # Sign-up button
    button_signup = tk.Button(signup_window, text="Sign Up", command=signup)
    button_signup.pack()
    signup_window.mainloop()

# Create the main window
window = tk.Tk()
window.title("Login")

# Load the image
image = tk.PhotoImage(file="main.png")

# Get the width and height of the image
image_width = image.width()
image_height = image.height()

# Set the maximum width for resizing
max_width = 700

# Calculate the appropriate window height to maintain image aspect ratio within the maximum width
window_height = int(image_height * max_width / image_width)

# Set the minimum and maximum window sizes
window.minsize(400, 400)  # Replace with your desired minimum size
window.maxsize(max_width, window_height)

# Create a label with the image as the background
background_label = tk.Label(window, image=image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# ID_number label and entry field
label_username = tk.Label(window, text="ID_number:")
label_username.pack()
entry_username = tk.Entry(window)
entry_username.pack(pady=(0, 10))

# Password label and entry field
label_password = tk.Label(window, text="Password:")
label_password.pack()
entry_password = tk.Entry(window, show="*")
entry_password.pack()

# Option box
option_var = tk.StringVar()
option_var.set("Readers") # Set a default option
option_box = tk.OptionMenu(window, option_var, "Staffs", "Readers")
option_box.pack()

# Login button
button_login = tk.Button(window, text="Login", command=login)
button_login.pack(pady=10)

# Sign-up section
label_signup = tk.Label(window, text="Oh, not a member yet?")
label_signup.pack()
button_signup = tk.Button(window, text="Sign Up", command=open_signup_window)
button_signup.pack(pady=10)

# Set padding for the window
window.config(padx=0, pady=0)

# Run the main event loop
window.mainloop()
