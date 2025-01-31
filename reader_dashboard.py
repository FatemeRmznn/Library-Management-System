import tkinter as tk
import pyodbc
from tkinter import ttk

# Connect to my SQL Server database
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-D5JS7NNP;'
    'DATABASE=Final_project;'
    'Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()


def open_Reader_dashboard(reader_id):
    def search_book():
        # Create a new window for book search
        search_window = tk.Toplevel()
        search_window.title("Search Book")
        # Load the image
        image = tk.PhotoImage(file="main.png")

        # Get the width and height of the image
        image_width = image.width()
        image_height = image.height()

        # Set the maximum width for resizing
        max_width = 710

        # Calculate the appropriate window height to maintain image aspect ratio within the maximum width
        window_height = int(image_height * max_width / image_width)

        # Set the minimum and maximum window sizes
        search_window.minsize(400, 400)  # Replace with your desired minimum size
        search_window.maxsize(max_width, window_height)

        # Create a label with the image as the background
        background_label = tk.Label(search_window, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create labels and entry fields for book title and ID
        label_title = tk.Label(search_window, text="Book Title:")
        entry_title = tk.Entry(search_window)
        label_title.pack()
        entry_title.pack()

        label_id = tk.Label(search_window, text="Book ID:")
        entry_id = tk.Entry(search_window)
        label_id.pack()
        entry_id.pack()

        def perform_search():
            # Retrieve the input values from the entry fields
            title = entry_title.get()
            book_id = entry_id.get()

            # Query the database based on the input values
            cursor.execute("SELECT * FROM book WHERE book_id = ? OR title = ?",
                           (book_id, title))
            rows = cursor.fetchall()

            # Clear the existing table data
            for record in search_table.get_children():
                search_table.delete(record)

            # Insert the fetched rows into the table
            for row in rows:
                ID_BOOK = row[0]
                Title = row[1]
                WriterName = row[2]
                PublisherID = row[3]
                PublisherYear = row[4]
                Number = row[5]
                Category = row[6]
                Detail = row[7]

                search_table.insert("", "end", values=(
                    ID_BOOK, Title, WriterName, PublisherID, PublisherYear, Number, Category, Detail))

        # Create a search button
        button_search = tk.Button(search_window, text="Search", command=perform_search)
        button_search.pack()

        # Create a treeview to display the records
        search_table = ttk.Treeview(search_window, columns=(
            "book_id", "title", "author", "publisher_id", "publication_year", "available", "category", "detail"))
        search_table.heading("book_id", text="book_id")
        search_table.heading("title", text="title")
        search_table.heading("author", text="author")
        search_table.heading("publisher_id", text="publisher_id")
        search_table.heading("publication_year", text="publication_year")
        search_table.heading("available", text="available")
        search_table.heading("category", text="category")
        search_table.heading("detail", text="detail")
        search_table.column("book_id", width=80)  # Set width for book_id column
        search_table.column("title", width=80)  # Set width for Title column
        search_table.column("author", width=100)  # Set width for Author column
        search_table.column("publisher_id", width=100)  # Set width for PublisherID column
        search_table.column("publication_year", width=100)  # Set width for PublishYear column
        search_table.column("available", width=80)  # Set width for Number column
        search_table.column("category", width=80)  # Set width for Category column
        search_table.column("detail", width=80)  # Set width for Detail column
        search_table.column("#0", width=0)  # Hide the first column
        search_table.place(x=0, y=0, relwidth=1, relheight=1)
        search_table.pack()

        search_window.mainloop()

    def open_books():
        # Execute the SQL query
        cursor.execute("SELECT * FROM Book")

        # Fetch all the rows from the query result
        rows = cursor.fetchall()

        # Clear the existing table data
        for record in book_table.get_children():
            book_table.delete(record)

        # Insert the fetched rows into the table
        for row in rows:
            book_id = row.ID_BOOK
            title = row.Title
            author = row.WriterName
            PublisherID = row.PublisherID
            PublishYear = row.PublishYear
            Number = row.Number
            Category = row.Category
            Detail = row.Detail

            # Insert the data into the table
            book_table.insert("", "end",
                              values=(book_id, title, author, PublisherID, PublishYear, Number, Category, Detail))

        # Show the table
        book_table.pack()

    def open_LendingDesk():
        # Create a new window for the Lending Desk
        lending_window = tk.Toplevel()
        lending_window.title("Lending Desk")

        # Load the image
        image = tk.PhotoImage(file="main.png")

        # Get the width and height of the image
        image_width = image.width()
        image_height = image.height()

        # Set the maximum width for resizing
        max_width = 600

        # Calculate the appropriate window height to maintain image aspect ratio within the maximum width
        window_height = int(image_height * max_width / image_width)

        # Set the minimum and maximum window sizes
        lending_window.minsize(400, 400)  # Replace with your desired minimum size
        lending_window.maxsize(max_width, window_height)

        # Create a label with the image as the background
        background_label = tk.Label(lending_window, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Define the columns for the Lending Desk table
        columns = ("book_id", "title", "borrow_description", "borrow_date", "return_date")

        # Create the Lending Desk table
        lending_table = ttk.Treeview(lending_window, columns=columns, show="headings")

        # Configure the column headings
        for col in columns:
            lending_table.heading(col, text=col)
            lending_table.column(col, width=100)  # Set the column width as desired

        sql_statement = f"""
            CREATE VIEW Reader_history AS
            SELECT L.book_id, B.title, L.borrow_description, L.borrow_date, L.return_date
            FROM LendingDesks L
            JOIN book B ON L.book_id = B.book_id
            WHERE L.reader_id = {reader_id}
        """
        cursor.execute(sql_statement)
        # Fetch the data from the Reader_history view
        cursor.execute("SELECT * FROM Reader_history")
        rows = cursor.fetchall()

        # Insert the data into the Lending Desk table
        for row in rows:
            lending_table.insert("", "end", values=row)

        # Pack the Lending Desk table
        lending_table.pack()
        lending_table.mainloop()

    dashboard = tk.Tk()
    dashboard.title("Reader dashboard")
    dashboard.geometry("700x500")

    button_search_book = tk.Button(dashboard, text="Search book", command=search_book)
    button_books = tk.Button(dashboard, text="See Books", command=open_books)
    button_LendingDesk = tk.Button(dashboard, text="Lending Desk", command=open_LendingDesk)

    # Place the buttons in the dashboard window
    button_search_book.pack()
    button_books.pack()
    button_LendingDesk.pack()

    # Create the table to display books (Initially hidden)
    book_table = ttk.Treeview(dashboard, columns=("book_id", "title", "Author", "PublisherID", "PublishYear", "Number",
                                                  "Category", "Detail"))
    book_table.heading("book_id", text="Book ID")
    book_table.heading("title", text="title")
    book_table.heading("Author", text="Author")
    book_table.heading("PublisherID", text="Publisher ID")
    book_table.heading("PublishYear", text="Publish Year")
    book_table.heading("Number", text="Number")
    book_table.heading("Category", text="Category")
    book_table.heading("Detail", text="Detail")
    book_table.column("book_id", width=80)  # Set width for book_id column
    book_table.column("title", width=80)  # Set width for Title column
    book_table.column("Author", width=80)  # Set width for Author column
    book_table.column("PublisherID", width=100)  # Set width for PublisherID column
    book_table.column("PublishYear", width=80)  # Set width for PublishYear column
    book_table.column("Number", width=80)  # Set width for Number column
    book_table.column("Category", width=80)  # Set width for Category column
    book_table.column("Detail", width=100)  # Set width for Detail column
    book_table.column("#0", width=0)  # Hide the first column

    # Create the table to display reports (Initially hidden)
    LendingDesk = ttk.Treeview(dashboard, columns=(
        "title", "Description", "Data Of Borrow", "Return Date"))
    LendingDesk.heading("title", text="title")
    LendingDesk.heading("Description", text="Description")
    LendingDesk.heading("Data Of Borrow", text="Data Of Borrow")
    LendingDesk.heading("Return Date", text="Return Date")
    dashboard.mainloop()



# if u need try reader dashboard u can use this part to run directly:

""""
dashboard = tk.Tk()
dashboard.title("Reader Dashboard")

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
dashboard.minsize(400, 400)  # Replace with your desired minimum size
dashboard.maxsize(max_width, window_height)

# Create a label with the image as the background
background_label = tk.Label(dashboard, image=image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a button to open the Reader dashboard
button_reader_dashboard = tk.Button(dashboard, text="Reader Dashboard", command=open_Reader_dashboard)
button_reader_dashboard.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Run the main event loop
dashboard.mainloop()
"""