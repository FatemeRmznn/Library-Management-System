import tkinter as tk
import pyodbc
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta


# Connect to my SQL Server database
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-D5JS7NNP;'
    'DATABASE=Final_project;'
    'Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()


def open_Staff_dashboard(Staff_ID):
    def add_new_book():
        def submit_book():
            # Get the entered values
            title = entry_title.get()
            writer_name = entry_writer.get()
            publisher_id = entry_publisher.get()
            publish_year = entry_year.get()
            number = entry_number.get()
            category = entry_category.get()
            details = entry_details.get()

            # Insert the new book into the database
            cursor.execute("INSERT INTO book "
                           "(title, author, publisher_id, publication_year, available, category, details) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (title, writer_name, publisher_id, publish_year, number, category, details))
            conn.commit()
            messagebox.showinfo("Success", "New book added successfully")

            sql_query = f"SELECT book_id FROM Book " \
                        f"WHERE title='{title}' AND author='{writer_name}' " \
                        f"AND publisher_id='{publisher_id}' " \
                        f"AND available='{number}' AND category='{category}' AND details='{details}'"

            # Execute the query
            cursor.execute(sql_query)
            results = cursor.fetchall()

            # Print the results
            for row in results:
                book_id = row.ID_BOOK

            # Close the cursor
            #cursor.close()

            current_date = datetime.now().date()
            sql_query2 = f"INSERT INTO Reports (detail, created_date, action_id, person_id) " \
                         f"VALUES ('added ' +'{title}' , '{current_date}', 'B '+ '{book_id}', 'S '+ '{Staff_ID}')"

            # Execute sql_query2
            cursor.execute(sql_query2)
            conn.commit()
            messagebox.showinfo("Success", "New record added successfully to report")

            # Close the add book window
            add_book_window.destroy()
        # Create a new window for adding a book
        add_book_window = tk.Toplevel()
        add_book_window.title("Add a new book")

        # Load the image
        image = tk.PhotoImage(file="main.png")

        # Get the width and height of the image
        image_width = image.width()
        image_height = image.height()

        # Set the maximum width for resizing
        max_width = 350

        # Calculate the appropriate window height to maintain image aspect ratio within the maximum width
        window_height = int(image_height * max_width / image_width)

        # Set the minimum and maximum window sizes
        add_book_window.minsize(240, 240)  # Replace with your desired minimum size
        add_book_window.maxsize(max_width, window_height)

        # Create a label with the image as the background
        background_label = tk.Label(add_book_window, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create labels and entry fields for book details
        label_title = tk.Label(add_book_window, text="Title:", width=30)
        entry_title = tk.Entry(add_book_window)

        label_writer = tk.Label(add_book_window, text="author:", width=30)
        entry_writer = tk.Entry(add_book_window)

        label_publisher = tk.Label(add_book_window, text="publisher_id:", width=30)
        entry_publisher = tk.Entry(add_book_window)

        label_year = tk.Label(add_book_window, text="publication year:", width=30)
        entry_year = tk.Entry(add_book_window)

        label_number = tk.Label(add_book_window, text="available:", width=30)
        entry_number = tk.Entry(add_book_window)

        label_category = tk.Label(add_book_window, text="category:", width=30)
        entry_category = tk.Entry(add_book_window)

        label_details = tk.Label(add_book_window, text="details:", width=30)
        entry_details = tk.Entry(add_book_window)

        # Create a submit button
        button_submit = tk.Button(add_book_window, text="Submit", command=submit_book)

        # Grid layout for labels and entry fields
        label_title.grid(row=0, column=0, sticky=tk.W)
        entry_title.grid(row=0, column=1)

        label_writer.grid(row=1, column=0, sticky=tk.W)
        entry_writer.grid(row=1, column=1)

        label_publisher.grid(row=2, column=0, sticky=tk.W)
        entry_publisher.grid(row=2, column=1)

        label_year.grid(row=3, column=0, sticky=tk.W)
        entry_year.grid(row=3, column=1)

        label_number.grid(row=4, column=0, sticky=tk.W)
        entry_number.grid(row=4, column=1)

        label_category.grid(row=5, column=0, sticky=tk.W)
        entry_category.grid(row=5, column=1)

        label_details.grid(row=6, column=0, sticky=tk.W)
        entry_details.grid(row=6, column=1)

        button_submit.grid(row=7, column=1)

        add_book_window.mainloop()

    def edit_book():
        # Create a new window for book search
        edit_book_window = tk.Toplevel()
        edit_book_window.title("Edit Book")
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
        edit_book_window.minsize(400, 400)  # Replace with your desired minimum size
        edit_book_window.maxsize(max_width, window_height)

        # Create a label with the image as the background
        background_label = tk.Label(edit_book_window, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create labels and entry fields for book title and ID
        label_bookID = tk.Label(edit_book_window, text="book_id")
        entry_bookID = tk.Entry(edit_book_window)
        label_bookID.pack()
        entry_bookID.pack()

        label_book_title = tk.Label(edit_book_window, text="title")
        entry_book_title = tk.Entry(edit_book_window)
        label_book_title.pack()
        entry_book_title.pack()

        def perform_editbook():
            # Retrieve the input values from the entry fields
            bookID = entry_bookID.get()
            bookTitle = entry_book_title.get()

            # Query the database based on the input values
            cursor.execute("SELECT * FROM Book WHERE book_id = ?  OR title = ? ",
                           (bookID), (bookTitle))
            rows = cursor.fetchall()

            # Clear the existing table data
            for record in book_table.get_children():
                book_table.delete(record)

            # Insert the fetched rows into the table
            for row in rows:
                BookID = row[0]
                Title = row[1]
                Author = row[2]
                PublisherID = row[3]
                PublishYear = row[4]
                Number = row[5]
                Category = row[6]
                Detail = row[7]

                book_table.insert("", "end", values=(
                    BookID, Title, Author, PublisherID, PublishYear, Number, Category, Detail))
            book_table.pack()

        button_edit_book_submit = tk.Button(edit_book_window, text="Search", command=perform_editbook)
        button_edit_book_submit.pack()

        # Option box
        option_var = tk.StringVar()
        option_var.set("Choose")  # Set a default option
        option_box = tk.OptionMenu(edit_book_window, option_var, "title", "author", "publisher_id",
                                   "publication_year", "available", "category", "details")

        label_update_book = tk.Label(edit_book_window, text="")
        entry_update_book = tk.Entry(edit_book_window)
        label_update_book.pack()
        entry_update_book.pack()
        option_box.pack()

        def submit_update_book():
            update_book = option_var.get()
            new_book_inform = entry_update_book.get()
            bookID = entry_bookID.get()
            print(update_book)
            print(new_book_inform)
            print(bookID)

            SQL_query = f"UPDATE Book SET " \
                        f" {update_book} = '{new_book_inform}' " \
                        f"  WHERE book_id = {bookID} "

            cursor.execute(SQL_query)
            print(SQL_query)
            conn.commit()
            messagebox.showinfo("Success", "Change applied.")
            current_date = datetime.now().date()
            sql_query2 = f"INSERT INTO Reports (detail, created_date, action_id, person_id) " \
                         f"VALUES ( 'change '+ '{update_book}' , '{current_date}'" \
                         f", 'B '+ '{bookID}', 'S '+ '{Staff_ID}')"

            # Execute sql_query2
            cursor.execute(sql_query2)
            conn.commit()
            messagebox.showinfo("Success", "New record added successfully to report")

        button_update_reader = tk.Button(edit_book_window, text="Submit edit", command=submit_update_book)
        button_update_reader.pack()
        # Create a search button

        edit_book_window.mainloop()

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
            book_id = row.book_id
            title = row.title
            author = row.author
            PublisherID = row.publisher_id
            PublishYear = row.publication_year
            Number = row.available
            Category = row.category
            Detail = row.details

            # Insert the data into the table
            book_table.insert("", "end", values=(book_id, title, author, PublisherID, PublishYear, Number, Category, Detail))

        # Show the table
        book_table.pack()

    def open_new_borrow():
        def submit_borrow():
            # Get the entered values
            book_id = entry_book_id.get()
            reader_id = entry_reader_id.get()
            date_of_borrowing = entry_date_of_borrowing.get()
            description = entry_description.get()
            borrow_date = datetime.strptime(date_of_borrowing, "%Y-%m-%d").date()
            return_date = borrow_date + timedelta(days=14)

            # Insert the new borrow record into the database
            sql_query1 = f"INSERT INTO LendingDesks " \
                         f"(book_id, reader_id, borrow_date, return_date, borrow_description) " \
                         f"VALUES ('{book_id}', '{reader_id}', '{borrow_date}', '{return_date}', '{description}')"

            cursor.execute(sql_query1)
            conn.commit()

            # Insert the new record into the Report table
            sql_query2 = f"INSERT INTO Reports (detail, created_date, action_id, person_id) " \
                         f"VALUES ('{description}', '{borrow_date}', 'B '+'{book_id}', 'R '+ '{reader_id}')"

            cursor.execute(sql_query2)
            conn.commit()

            messagebox.showinfo("Success", "New borrow record added successfully")

            # Close the add borrow window
            add_borrow_window.destroy()

        # Create a new window for adding a borrow record
        add_borrow_window = tk.Toplevel()
        add_borrow_window.title("Add a new borrow record")

        # Create labels and entry fields for borrow details
        label_book_id = tk.Label(add_borrow_window, text="book_id:")
        entry_book_id = tk.Entry(add_borrow_window)

        label_reader_id = tk.Label(add_borrow_window, text="reader_id:")
        entry_reader_id = tk.Entry(add_borrow_window)

        label_date_of_borrowing = tk.Label(add_borrow_window, text="Date of Borrowing:")
        entry_date_of_borrowing = tk.Entry(add_borrow_window)

        label_description = tk.Label(add_borrow_window, text="Description")
        entry_description = tk.Entry(add_borrow_window)
        # Create a submit button
        button_submit = tk.Button(add_borrow_window, text="Submit", command=submit_borrow)

        # Grid layout for labels and entry fields
        label_book_id.grid(row=0, column=0, sticky=tk.E)
        entry_book_id.grid(row=0, column=1)

        label_reader_id.grid(row=1, column=0, sticky=tk.E)
        entry_reader_id.grid(row=1, column=1)

        label_date_of_borrowing.grid(row=2, column=0, sticky=tk.E)
        entry_date_of_borrowing.grid(row=2, column=1)

        label_description.grid(row=3, column=0, sticky=tk.E)
        entry_description.grid(row=3, column=1)

        button_submit.grid(row=4, column=1)

    def edit_borrow():
        # Create a new window for book search
        edit_borrow_window = tk.Toplevel()
        edit_borrow_window.title("Edit Borrow")
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
        edit_borrow_window.minsize(400, 400)  # Replace with your desired minimum size
        edit_borrow_window.maxsize(max_width, window_height)
        # Create a label with the image as the background
        background_label = tk.Label(edit_borrow_window, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create labels and entry fields for book title and ID
        label_bookID = tk.Label(edit_borrow_window, text="book_id")
        entry_bookID = tk.Entry(edit_borrow_window)
        label_bookID.pack()
        entry_bookID.pack()

        label_readerID = tk.Label(edit_borrow_window, text="reader_id")
        entry_readerID = tk.Entry(edit_borrow_window)
        label_readerID.pack()
        entry_readerID.pack()

        def perform_edit_borrow():
            # Retrieve the input values from the entry fields
            bookID = entry_bookID.get()
            readerID = entry_readerID.get()

            # Query the database based on the input values
            cursor.execute("SELECT * FROM LendingDesks WHERE book_id = ?  AND reader_id = ? ",
                           (bookID), (readerID))
            rows = cursor.fetchall()
            print(rows)
            # Clear the existing table data
            for record in Lending_table.get_children():
                Lending_table.delete(record)

            # Insert the fetched rows into the table
            for row in rows:
                LendingID = row[5]
                ID_BOOK = row[0]
                ID_READER = row[1]
                DescriptionOfBorrow = row[2]
                BORROW_DATE = row[3]
                RETURN_DATE = row[4]
                print(row)

                Lending_table.insert("", "end", values=(
                        LendingID, ID_BOOK, ID_READER, DescriptionOfBorrow, BORROW_DATE, RETURN_DATE))
                Lending_table.pack()

        button_edit_lending_submit = tk.Button(edit_borrow_window, text="Search", command=perform_edit_borrow)
        button_edit_lending_submit.pack()

        # Option box
        option_var = tk.StringVar()
        option_var.set("Choose")  # Set a default option
        option_box = tk.OptionMenu(edit_borrow_window, option_var, "borrow_description", "return_date")

        label_update_borrow = tk.Label(edit_borrow_window, text="")
        entry_update_borrow = tk.Entry(edit_borrow_window)
        label_update_borrow.pack()
        entry_update_borrow.pack()
        option_box.pack()

        def submit_update_borrow():
            update_borrow = option_var.get()
            new_borrow_inform = entry_update_borrow.get()
            bookID = entry_bookID.get()
            readerID= entry_readerID.get()
            SQL_query = f"UPDATE LendingDesks SET " \
                        f" {update_borrow} = '{new_borrow_inform}' " \
                        f"  WHERE book_id = {bookID} AND reader_id = {readerID} "

            cursor.execute(SQL_query)
            conn.commit()
            messagebox.showinfo("Success", "Change applied.")
            current_date = datetime.now().date()
            sql_query2 = f"INSERT INTO Reports (detail, created_date, action_id, person_id) " \
                         f"VALUES ( 'change '+ '{update_borrow}' , '{current_date}'" \
                         f", 'B '+ '{bookID}', 'S '+ '{Staff_ID}')"

            # Execute sql_query2
            cursor.execute(sql_query2)
            conn.commit()
            messagebox.showinfo("Success", "New record added successfully to report")

        button_update_borrow = tk.Button(edit_borrow_window, text="Submit edit", command=submit_update_borrow)
        button_update_borrow.pack()
        # Create a search button

        edit_borrow_window.mainloop()

    def open_publisher():
        # Execute the SQL query
        cursor.execute("SELECT * FROM Publishers")

        # Fetch all the rows from the query result
        rows = cursor.fetchall()

        # Clear the existing table data
        for record in publisher_table.get_children():
            publisher_table.delete(record)
            # Insert the fetched rows into the table
        for row in rows:
            publisher_id = row.publisher_id
            name = row.publisher_id
            address = row.address
            EstablishedYear = row.established_year
            ContactEmail = row.contact_number

            # Insert the data into the table
            publisher_table.insert("", "end",
                                       values=(publisher_id, name, address, EstablishedYear, ContactEmail))

        # Show the table
        publisher_table.pack()

    def add_new_publisher():
        def submit_publisher():
            # Get the entered values
            name = entry_name.get()
            address = entry_address.get()
            start_year = entry_start_year.get()
            contact = entry_contact.get()


            # Insert the new publisher into the database
            cursor.execute("INSERT INTO Publishers "
                           "(publisher_name, [address], established_year, contact_number) "
                           "VALUES (?, ?, ?, ?)",
                           (name, address, start_year, contact))
            conn.commit()
            messagebox.showinfo("Success", "New Publisher added successfully")

            sql_query = f"SELECT publisher_id FROM Publishers " \
                        f"WHERE publisher_name='{name}' AND [address]='{address}' " \
                        f"AND established_year='{start_year}' " \
                        f"AND contact_number='{contact}'"

            # Execute the query
            cursor.execute(sql_query)
            results = cursor.fetchall()

            # Print the results
            for row in results:
                publisher_id= row.PublisherID

            # Close the cursor
            #cursor.close()
            details= "add "+name
            current_date = datetime.now().date()
            sql_query2 = f"INSERT INTO Reports (detail, created_date, action_id, person_id) " \
                         f"VALUES ('added ' + '{name}', '{current_date}', 'P '+ '{publisher_id}', 'S ' + '{Staff_ID}')"

            # Execute sql_query2
            cursor.execute(sql_query2)
            conn.commit()
            messagebox.showinfo("Success", "New record added successfully to report")

            # Close the add book window
            add_publisher_window.destroy()

        # Create a new window for adding a book
        add_publisher_window = tk.Toplevel()
        add_publisher_window.title("Add a new publisher")

        # Load the image
        image = tk.PhotoImage(file="main.png")

        # Get the width and height of the image
        image_width = image.width()
        image_height = image.height()

        # Set the maximum width for resizing
        max_width = 350

        # Calculate the appropriate window height to maintain image aspect ratio within the maximum width
        window_height = int(image_height * max_width / image_width)

        # Set the minimum and maximum window sizes
        add_publisher_window.minsize(240, 240)  # Replace with your desired minimum size
        add_publisher_window.maxsize(max_width, window_height)

        # Create a label with the image as the background
        background_label = tk.Label(add_publisher_window, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create labels and entry fields for book details
        label_name = tk.Label(add_publisher_window, text="publisher name:", width=30)
        entry_name = tk.Entry(add_publisher_window)

        label_address = tk.Label(add_publisher_window, text="address", width=30)
        entry_address = tk.Entry(add_publisher_window)

        label_start_year = tk.Label(add_publisher_window, text="established year:", width=30)
        entry_start_year = tk.Entry(add_publisher_window)

        label_contact = tk.Label(add_publisher_window, text="contact_number:", width=30)
        entry_contact = tk.Entry(add_publisher_window)

        # Create a submit button
        button_submit = tk.Button(add_publisher_window, text="Submit", command=submit_publisher)

        # Grid layout for labels and entry fields
        label_name.grid(row=0, column=0, sticky=tk.W)
        entry_name.grid(row=0, column=1)

        label_address.grid(row=1, column=0, sticky=tk.W)
        entry_address.grid(row=1, column=1)

        label_start_year.grid(row=2, column=0, sticky=tk.W)
        entry_start_year.grid(row=2, column=1)

        label_contact.grid(row=3, column=0, sticky=tk.W)
        entry_contact.grid(row=3, column=1)

        button_submit.grid(row=4, column=1)

        add_publisher_window.mainloop()

    def hide_table():
        book_table.pack_forget()
        reports_table.pack_forget()
        publisher_table.pack_forget()
        reader_table.pack_forget()
        Lending_table.pack_forget()

    def open_reports():
        # Execute the SQL query
        cursor.execute("SELECT * FROM Reports")

        # Fetch all the rows from the query result
        rows = cursor.fetchall()

        # Clear the existing table data
        for record in reports_table.get_children():
            reports_table.delete(record)

        # Insert the fetched rows into the table
        for row in rows:
            report_id = row.report_id
            detail = row.detail
            DateCreated = row.created_date
            ActionID = row.action_id
            PersonID = row.person_id

            # Insert the data into the table
            reports_table.insert("", "end", values=(report_id, detail, DateCreated, ActionID, PersonID))

        # Show the table
        reports_table.pack()

    def open_user():
        # Execute the SQL query
        cursor.execute("SELECT * FROM Readers")

        # Fetch all the rows from the query result
        rows = cursor.fetchall()

        # Clear the existing table data
        for record in reader_table.get_children():
            reader_table.delete(record)

        # Insert the fetched rows into the table
        for row in rows:
            read_id = row.reader_id
            F_name = row.first_name
            L_name = row.last_name
            r_username = row.ID_number
            r_pass = row.password
            r_phonenumber = row.phone_number
            address = row.address


            # Insert the data into the table
            reader_table.insert("", "end",
                              values=(read_id, F_name, L_name, r_username, r_pass, r_phonenumber, address))

        # Show the table
        reader_table.pack()

    def add_new_reader():
        def submit_reader():
            # Get the entered values
            FirstName = entry_FirstName.get()
            LastName = entry_LastName.get()
            Username = entry_Username.get()
            Pass = entry_Pass.get()
            PhoneNumber = entry_PhoneNumber.get()
            Adderss = entry_Adderss.get()

            # Insert the new book into the database
            cursor.execute("INSERT INTO Readers "
                           "(first_name, last_name, ID_number, [password], phone_number, [address]) "
                           "VALUES (?, ?, ?, ?, ?, ?)",
                           (FirstName, LastName, Username, Pass, PhoneNumber, Adderss))
            conn.commit()
            messagebox.showinfo("Success", "New reader added successfully")

            sql_query = f"SELECT reader_id FROM Readers " \
                        f"WHERE first_name='{FirstName}' AND last_name='{LastName}' " \
                        f"AND ID_number='{Username}' " \
                        f"AND [password]='{Pass}' AND phone_number='{PhoneNumber}' "

            # Execute the query
            cursor.execute(sql_query)
            results = cursor.fetchall()

            # Print the results
            for row in results:
                reader_id = row.reader_id

            # Close the cursor
            # cursor.close()

            current_date = datetime.now().date()
            sql_query2 = f"INSERT INTO Reports (detail, created_date, action_id, person_id) " \
                         f"VALUES ( 'added', '{current_date}', 'R '+ '{reader_id}', 'S '+ '{Staff_ID}')"

            # Execute sql_query2
            cursor.execute(sql_query2)
            conn.commit()
            messagebox.showinfo("Success", "New record added successfully to report")

            # Close the add book window
            add_reader_window.destroy()

        # Create a new window for adding a book
        add_reader_window = tk.Toplevel()
        add_reader_window.title("Add a new Reader")

        # Load the image
        image = tk.PhotoImage(file="main.png")

        # Get the width and height of the image
        image_width = image.width()
        image_height = image.height()

        # Set the maximum width for resizing
        max_width = 350

        # Calculate the appropriate window height to maintain image aspect ratio within the maximum width
        window_height = int(image_height * max_width / image_width)

        # Set the minimum and maximum window sizes
        add_reader_window.minsize(240, 240)  # Replace with your desired minimum size
        add_reader_window.maxsize(max_width, window_height)

        # Create a label with the image as the background
        background_label = tk.Label(add_reader_window, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create labels and entry fields for book details
        label_FirstName = tk.Label(add_reader_window, text="First name:", width=30)
        entry_FirstName = tk.Entry(add_reader_window)

        label_LastName = tk.Label(add_reader_window, text="Last name:", width=30)
        entry_LastName = tk.Entry(add_reader_window)

        label_Username = tk.Label(add_reader_window, text="ID_number:", width=30)
        entry_Username = tk.Entry(add_reader_window)

        label_Pass = tk.Label(add_reader_window, text="password:", width=30)
        entry_Pass = tk.Entry(add_reader_window)

        label_PhoneNumber = tk.Label(add_reader_window, text="phone_number:", width=30)
        entry_PhoneNumber = tk.Entry(add_reader_window)

        label_Adderss = tk.Label(add_reader_window, text="[address]:", width=30)
        entry_Adderss = tk.Entry(add_reader_window)

        # Create a submit button
        button_submit = tk.Button(add_reader_window, text="Submit", command=submit_reader)

        # Grid layout for labels and entry fields
        label_FirstName.grid(row=0, column=0, sticky=tk.W)
        entry_FirstName.grid(row=0, column=1)

        label_LastName.grid(row=1, column=0, sticky=tk.W)
        entry_LastName.grid(row=1, column=1)

        label_Username.grid(row=2, column=0, sticky=tk.W)
        entry_Username.grid(row=2, column=1)

        label_Pass.grid(row=3, column=0, sticky=tk.W)
        entry_Pass.grid(row=3, column=1)

        label_PhoneNumber.grid(row=4, column=0, sticky=tk.W)
        entry_PhoneNumber.grid(row=4, column=1)

        label_Adderss.grid(row=5, column=0, sticky=tk.W)
        entry_Adderss.grid(row=5, column=1)

        button_submit.grid(row=6, column=1)

        add_reader_window.mainloop()

    def edit_reader():
        # Create a new window for book search
        edit_reader_window = tk.Toplevel()
        edit_reader_window.title("Edit Reader")
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
        edit_reader_window.minsize(400, 400)  # Replace with your desired minimum size
        edit_reader_window.maxsize(max_width, window_height)

        # Create a label with the image as the background
        background_label = tk.Label(edit_reader_window, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create labels and entry fields for book title and ID
        label_readerID = tk.Label(edit_reader_window, text="reader_id")
        entry_readerID = tk.Entry(edit_reader_window)
        label_readerID.pack()
        entry_readerID.pack()

        def perform_edit():
            # Retrieve the input values from the entry fields
            readerID = entry_readerID.get()

            # Query the database based on the input values
            cursor.execute("SELECT * FROM Readers WHERE reader_id = ? ",
                           (readerID))
            rows = cursor.fetchall()
            print(rows)

            # Clear the existing table data
            for record in reader_table.get_children():
                reader_table.delete(record)

            # Insert the fetched rows into the table
            for row in rows:
                ReaderID = row[0]
                FirstName = row[1]
                LastName = row[2]
                Username = row[3]
                Pass = row[4]
                PhoneNumber = row[5]
                Adderss = row[6]

                reader_table.insert("", "end", values=(
                    ReaderID, FirstName, LastName, Username, Pass, PhoneNumber, Adderss))
            reader_table.pack()

        button_edit_submit = tk.Button(edit_reader_window, text="Search", command=perform_edit)
        button_edit_submit.pack()

        # Option box
        option_var = tk.StringVar()
        option_var.set("Choose")  # Set a default option
        option_box = tk.OptionMenu(edit_reader_window, option_var, "first_name", "last_name", "[password]",
                                   "phone_number", "[address]")

        label_update_reader = tk.Label(edit_reader_window, text="")
        entry_update_reader = tk.Entry(edit_reader_window)
        label_update_reader.pack()
        entry_update_reader.pack()
        option_box.pack()

        def submit_update():
            update_reader = option_var.get()
            new_reader_inform = entry_update_reader.get()

            readerID= entry_readerID.get()
            SQL_query= f"UPDATE Readers SET " \
                       f" {update_reader} = '{new_reader_inform}' " \
                       f"  WHERE reader_id = '{readerID}' "

            cursor.execute(SQL_query)
            conn.commit()
            messagebox.showinfo("Success", "Change applied.")
            current_date = datetime.now().date()
            sql_query2 = f"INSERT INTO Reports (detail, created_date, action_id, person_id) " \
                         f"VALUES ( 'change '+ '{update_reader}' , '{current_date}'" \
                         f", 'R '+ '{readerID}', 'S '+ '{Staff_ID}')"

            # Execute sql_query2
            cursor.execute(sql_query2)
            conn.commit()
            messagebox.showinfo("Success", "New record added successfully to report")

        button_update_reader = tk.Button(edit_reader_window, text="Submit edit", command=submit_update)
        button_update_reader.pack()

    dashboard = tk.Toplevel()
    dashboard.geometry('800x500')
    dashboard.title("Staff Dashboard")

    # Create the buttons
    button_books = tk.Button(dashboard, text="Books", command=open_books, width=20)
    button_reader = tk.Button(dashboard, text="Reader", command=open_user, width=20)
    button_add_reader = tk.Button(dashboard, text="Add a new reader", command=add_new_reader, width=20)
    button_edit_reader = tk.Button(dashboard, text="Edit reader information", command=edit_reader, width=20)
    button_search_book = tk.Button(dashboard, text="Search book", command=edit_book, width=20)
    button_add_book = tk.Button(dashboard, text="Add a new book", command=add_new_book, width=20)
    button_new_borrow = tk.Button(dashboard, text="Add a new borrow recorde", command=open_new_borrow, width=20)
    button_old_borrow = tk.Button(dashboard, text="Edit an existing record ", command=edit_borrow, width=20)
    button_publisher = tk.Button(dashboard, text="Publisher", command=open_publisher, width=20)
    button_add_publisher = tk.Button(dashboard, text="Add a new publisher", command=add_new_publisher, width=20)
    button_reports = tk.Button(dashboard, text="Reports", command=open_reports, width=20)
    button_close = tk.Button(dashboard, text="Close table ", command=hide_table, width=20)

    # Place the buttons in the dashboard window
    button_add_book.pack()
    button_reader.pack()
    button_add_reader.pack()
    button_edit_reader.pack()
    button_search_book.pack()
    button_books.pack()
    button_new_borrow.pack()
    button_old_borrow.pack()
    button_publisher.pack()
    button_add_publisher.pack()
    button_reports.pack()
    button_close.pack()
    # Create the table to display books (Initially hidden)

    book_table = ttk.Treeview(dashboard, columns=("book_id", "title", "author", "publisher_id", "publication_year",
                                                  "available", "category", "detail"))
    book_table.heading("book_id", text="book ID")
    book_table.heading("title", text="title")
    book_table.heading("author", text="author")
    book_table.heading("publisher_id", text="publisher_id")
    book_table.heading("publication_year", text="publication year")
    book_table.heading("available", text="available")
    book_table.heading("category", text="category")
    book_table.heading("detail", text="detail")

    book_table.column("book_id", width=80 )
    book_table.column("title", width=80)
    book_table.column("author", width=100)
    book_table.column("publisher_id", width=100)
    book_table.column("publication_year", width=100)
    book_table.column("available", width=80)
    book_table.column("category", width=80)
    book_table.column("detail", width=80)
    book_table.column("#0", width=0)  # Hide the first column

    # Create the table to display user (Initially hidden)
    reader_table = ttk.Treeview(dashboard, columns=("reader_id", "first_name", "last_name", "ID_number", "[password]",
                                                    "phone_number", "[address]"))
    reader_table.heading("reader_id", text="reader_id" )
    reader_table.heading("first_name", text="First name")
    reader_table.heading("last_name", text="Last name")
    reader_table.heading("ID_number", text="ID_number")
    reader_table.heading("[password]", text="Password")
    reader_table.heading("phone_number", text="PhoneNumber")
    reader_table.heading("[address]", text="Address")

    reader_table.column("reader_id", width=80 )
    reader_table.column("first_name", width=80)
    reader_table.column("last_name", width=100)
    reader_table.column("ID_number", width=100)
    reader_table.column("[password]", width=100)
    reader_table.column("phone_number", width=80)
    reader_table.column("[address]", width=80)
    reader_table.column("#0", width=0)  # Hide the first column

    # Create the table to display publishers (Initially hidden)
    publisher_table = ttk.Treeview(dashboard, columns=(
        "publisher_id", "publisher_name", "[address]", "established_year", "contact_number"))
    publisher_table.heading("publisher_id", text="Publisher ID")
    publisher_table.heading("publisher_name", text="Name")
    publisher_table.heading("[address]", text="Address")
    publisher_table.heading("established_year", text="established year")
    publisher_table.heading("contact_number", text="contact_number Email")

    publisher_table.column("publisher_id", width=150)
    publisher_table.column("publisher_name", width=150)
    publisher_table.column("[address]", width=150)
    publisher_table.column("established_year", width=150)
    publisher_table.column("contact_number", width=150)
    publisher_table.column("#0", width=0)  # Hide the first column

    # Create the table to display reports (Initially hidden)
    reports_table = ttk.Treeview(dashboard, columns=(
        "report_id", "detail", "created_date", "action_id", "person_id"))
    reports_table.heading("report_id", text="report_id")
    reports_table.heading("detail", text="detail")
    reports_table.heading("created_date", text="created date")
    reports_table.heading("action_id", text="action_id")
    reports_table.heading("person_id", text="person_id")

    reports_table.column("report_id", width=150)
    reports_table.column("detail", width=150)
    reports_table.column("created_date", width=150)
    reports_table.column("action_id", width=150)
    reports_table.column("person_id", width=150)
    reports_table.column("#0", width=0)  # Hide the first column

    # Create the table to display Lending (Initially hidden)
    Lending_table = ttk.Treeview (dashboard, columns= ("lending_id", "book_id", "reader_id", "borrow_description",
                                                       "borrow_date", "return_date"))
    Lending_table.heading("lending_id", text="lending_id")
    Lending_table.heading("book_id", text="book_id")
    Lending_table.heading("reader_id", text="reader_id")
    Lending_table.heading("borrow_description", text="borrow_description")
    Lending_table.heading("borrow_date", text="borrow_date")
    Lending_table.heading("return_date", text="return_date")

    Lending_table.column("lending_id", width=80)
    Lending_table.column("book_id", width=80)
    Lending_table.column("reader_id", width=80)
    Lending_table.column("borrow_description",width=150)
    Lending_table.column("borrow_date", width=150)
    Lending_table.column("return_date", width=150)
    Lending_table.column("#0", width=0)  # Hide the first column)

    dashboard.mainloop()

# if u need try reader dashboard u can use this part to run directly:

""""

dashboard = tk.Tk()
dashboard.geometry('500x500')
dashboard.title("Staff Dashboard")

# Create a button to open the Staff dashboard
button_staff_dashboard = tk.Button(dashboard, text="Staff Dashboard", command=open_Staff_dashboard)
button_staff_dashboard.pack()

dashboard.mainloop()
"""