import tkinter as tk
import pyodbc
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox

# Connect to my SQL Server database
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-D5JS7NNP;'
    'DATABASE=Library_Management;'
    'Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()


# --- Helper Functions ---
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")


def load_background(window, image_path, width, height):
    try:
        image = Image.open(image_path)
        resized_image = image.resize((width, height), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(resized_image)

        # نگه‌داشتن مرجع به تصویر
        window.bg_image = bg_image

        background_label = tk.Label(window, image=bg_image)
        background_label.image = bg_image  # Keep a reference!
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        return background_label  # return label
    except FileNotFoundError:
        messagebox.showerror("Error", f"Image file '{image_path}' not found.")
        return None


def apply_font(widget, font_style):
    widget.config(font=font_style)


def create_label(window, text, font_style, bg="white", **kwargs):
    label = tk.Label(window, text=text, font=font_style, bg=bg, **kwargs)
    return label


def create_entry(window, font_style, **kwargs):
    entry = tk.Entry(window, font=font_style, **kwargs)
    return entry


def create_button(window, text, command, font_style, **kwargs):
    button = tk.Button(window, text=text, command=command, font=font_style, **kwargs)
    return button


def create_treeview(window, columns, heading_texts, column_widths, font_style):
    style = ttk.Style()
    style.configure("Treeview", font=font_style)  # تنظیم فونت برای Treeview
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  # تنظیم فونت هدر

    tree = ttk.Treeview(window, columns=columns, show="headings", style="Treeview")
    for col, heading_text, width in zip(columns, heading_texts, column_widths):
        tree.heading(col, text=heading_text)
        tree.column(col, width=width)

    return tree


# --- End Helper Functions ---


def open_reader_dashboard(reader_id):
    DASHBOARD_WIDTH = 900
    DASHBOARD_HEIGHT = 600
    FONT_STYLE = ("Arial", 12)

    dashboard = tk.Toplevel()
    dashboard.title("Reader Dashboard")
    center_window(dashboard, DASHBOARD_WIDTH, DASHBOARD_HEIGHT)

    # Load Background Image
    background_label = load_background(dashboard, "library.jpg", DASHBOARD_WIDTH, DASHBOARD_HEIGHT)
    if not background_label:
        return

    # ایجاد Frame مخفی برای نمایش محتوا
    search_frame = tk.Frame(dashboard, bg="white")
    search_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    search_frame.pack_forget()  # در ابتدا مخفی باشد

    def show_frame():
        """ این تابع باعث می‌شود که Frame دیده شود. """
        search_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def search_book():
        search_frame.pack_forget()
        for widget in search_frame.winfo_children():
            widget.destroy()

        show_frame()

        label_title = create_label(search_frame, "Book Title:", FONT_STYLE, bg="white")
        label_title.pack(pady=(20, 5))
        entry_title = create_entry(search_frame, FONT_STYLE)
        entry_title.pack(pady=(0, 10))

        label_id = create_label(search_frame, "Book ID:", FONT_STYLE, bg="white")
        label_id.pack(pady=(5, 5))
        entry_id = create_entry(search_frame, FONT_STYLE)
        entry_id.pack(pady=(0, 10))

        def perform_search():
            book_id = entry_id.get().strip()
            title = entry_title.get().strip()

            # بررسی اینکه حداقل یک مقدار وارد شده باشد
            if not book_id and not title:
                messagebox.showwarning("Warning", "Please enter either Book ID or Title.")
                return

            try:
                query = "SELECT * FROM Books WHERE 1=1"
                params = []

                if book_id:
                    query += " AND book_id = ?"
                    params.append(book_id)

                if title:
                    query += " AND title LIKE ?"
                    params.append(f"%{title}%")

                cursor.execute(query, params)
                rows = cursor.fetchall()

                # حذف داده‌های قبلی `Treeview`
                for record in search_table.get_children():
                    search_table.delete(record)

                if not rows:
                    messagebox.showinfo("Search Result", "No books found.")
                    return

                for row in rows:
                    search_table.insert("", "end", values=(
                        row.book_id,
                        row.title,
                        row.author,
                        row.publisher_id,
                        row.publication_year,
                        "Yes" if row.available else "No",
                        row.category if row.category else "",
                        row.details if row.details else ""
                    ))

            except pyodbc.Error as e:
                messagebox.showerror("Database Error", f"Error searching for books: {e}")

        button_search = create_button(search_frame, "Search", perform_search, FONT_STYLE)
        button_search.pack(pady=20)

        search_table = create_treeview(
            search_frame,
            columns=(
            "book_id", "title", "author", "publisher_id", "publication_year", "available", "category", "details"),
            heading_texts=(
            "Book ID", "Title", "Author", "Publisher ID", "Publication Year", "Available", "Category", "Details"),
            column_widths=(80, 120, 100, 100, 100, 80, 120, 150),
            font_style=FONT_STYLE
        )
        search_table.column("#0", width=0, stretch=tk.NO)
        search_table.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)



    def open_books():
        search_frame.pack_forget()
        for widget in search_frame.winfo_children():
            widget.destroy()

        show_frame()

        label_books = create_label(search_frame, "Available Books:", FONT_STYLE, bg="white")
        label_books.pack(pady=(10, 5))

        book_table = create_treeview(
            search_frame,
            columns=(
            "book_id", "title", "author", "publisher_id", "publication_year", "available", "category", "details"),
            heading_texts=(
            "Book ID", "Title", "Author", "Publisher ID", "Publication Year", "Available", "Category", "Details"),
            column_widths=(80, 120, 100, 100, 100, 80, 120, 150),
            font_style=FONT_STYLE
        )
        book_table.column("#0", width=0, stretch=tk.NO)
        book_table.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        try:
            cursor.execute("SELECT * FROM Books")
            rows = cursor.fetchall()

            # پاک کردن داده‌های قبلی از `Treeview`
            for record in book_table.get_children():
                book_table.delete(record)

            for row in rows:
                # جایگزینی مقدار `None` با مقدار خالی برای جلوگیری از خطای `NoneType`
                book_table.insert("", "end", values=(
                    row.book_id,
                    row.title,
                    row.author,
                    row.publisher_id,
                    row.publication_year,
                    "Yes" if row.available else "No",
                    row.category if row.category else "",
                    row.details if row.details else ""
                ))

        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Error fetching book data: {e}")

    def open_lending_desk():
        search_frame.pack_forget()
        for widget in search_frame.winfo_children():
            widget.destroy()

        show_frame()

        label_history = create_label(search_frame, "Lending History:", FONT_STYLE, bg="white")
        label_history.pack(pady=(10, 5))

        columns = ("book_id", "title", "borrow_date", "return_date", "remarks", "reader_name", "status")
        lending_table = create_treeview(
            search_frame,
            columns=columns,
            heading_texts=("Book ID", "Title", "Borrow Date", "Return Date", "Remarks", "Reader", "Status"),
            column_widths=(80, 150, 120, 120, 120, 150, 100),
            font_style=FONT_STYLE
        )
        lending_table.column("#0", width=0, stretch=tk.NO)
        lending_table.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        try:
            query = """
                SELECT 
                    L.book_id, 
                    B.title, 
                    CONVERT(VARCHAR, L.borrow_date, 120) AS borrow_date,
                    COALESCE(CONVERT(VARCHAR, L.return_date, 120), 'Not Returned') AS return_date,
                    COALESCE(L.remarks, '') AS remarks,
                    R.first_name + ' ' + R.last_name AS reader_name,
                    CASE 
                        WHEN L.return_date IS NULL THEN 'Borrowed'
                        ELSE 'Returned'
                    END AS status
                FROM LendingDesk L
                LEFT JOIN Books B ON L.book_id = B.book_id
                LEFT JOIN Readers R ON L.reader_id = R.reader_id
                WHERE L.reader_id = ?
            """

            cursor.execute(query, (reader_id,))
            rows = cursor.fetchall()

            # پاک کردن داده‌های قبلی از Treeview
            for record in lending_table.get_children():
                lending_table.delete(record)

            # درج داده‌ها در Treeview
            for row in rows:
                lending_table.insert("", "end", values=row)

        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Error fetching lending history: {e}")

    # دکمه‌ها
    button_search_book = create_button(dashboard, "Search Book", search_book, FONT_STYLE)
    button_books = create_button(dashboard, "See Books", open_books, FONT_STYLE)
    button_lending_desk = create_button(dashboard, "Lending Desk", open_lending_desk, FONT_STYLE)

    button_search_book.pack(pady=10)
    button_books.pack(pady=10)
    button_lending_desk.pack(pady=10)

if __name__ == '__main__':
    open_reader_dashboard(123)
