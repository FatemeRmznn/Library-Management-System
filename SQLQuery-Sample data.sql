-- 1. وارد کردن داده‌های نمونه برای ناشران (Publishers)
INSERT INTO Publishers (publisher_name, [address], established_year, contact_number)
VALUES 
('Penguin Books', 'New York, USA', 1935, '123-456-7890'),
('HarperCollins', 'London, UK', 1817, '987-654-3210'),
('Oxford Press', 'Oxford, UK', 1478, '555-555-5555'),
('Scholastic', 'Toronto, Canada', 1920, '111-222-3333'),
('Simon & Schuster', 'New York, USA', 1924, '999-888-7777'),
('Macmillan', 'Berlin, Germany', 1843, '666-777-8888'),
('Springer', 'Heidelberg, Germany', 1842, '333-444-5555'),
('Cambridge Press', 'Cambridge, UK', 1534, '123-321-1234'),
('Hachette', 'Paris, France', 1826, '777-666-5555'),
('Random House', 'New York, USA', 1927, '444-333-2222');

-- 2. وارد کردن داده‌های نمونه برای کتاب‌ها (Books)
INSERT INTO Books (title, author, publisher_id, publication_year, available, category, details)
VALUES 
('To Kill a Mockingbird', 'Harper Lee', 1, 1960, 1, 'Fiction', 'Classic novel about racism in America'),
('1984', 'George Orwell', 2, 1949, 1, 'Dystopian', 'A novel about totalitarianism'),
('The Great Gatsby', 'F. Scott Fitzgerald', 3, 1925, 1, 'Classic', 'Story about the American dream'),
('Pride and Prejudice', 'Jane Austen', 4, 1813, 1, 'Romance', 'Classic love story'),
('Moby Dick', 'Herman Melville', 5, 1851, 1, 'Adventure', 'A novel about a giant whale'),
('War and Peace', 'Leo Tolstoy', 6, 1869, 1, 'Historical', 'A book about the Napoleonic Wars'),
('Harry Potter', 'J.K. Rowling', 7, 1997, 1, 'Fantasy', 'A wizard’s journey in Hogwarts'),
('The Hobbit', 'J.R.R. Tolkien', 8, 1937, 1, 'Fantasy', 'Prequel to Lord of the Rings'),
('Brave New World', 'Aldous Huxley', 9, 1932, 1, 'Dystopian', 'A futuristic dystopia'),
('The Catcher in the Rye', 'J.D. Salinger', 10, 1951, 1, 'Young Adult', 'Story about teenage angst');

-- 3. وارد کردن داده‌های نمونه برای کاربران (Readers)
INSERT INTO Readers (first_name, last_name, ID_number, password_hash, phone_number, [address], registration_date)
VALUES 
('Ali', 'Ahmadi', '1234567890', 'pass1', '09121234567', 'Tehran, Iran', '2023-01-10'),
('Sara', 'Mohammadi', '0987654321', 'pass2', '09127654321', 'Shiraz, Iran', '2023-02-15'),
('Reza', 'Karimi', '1122334455', 'pass3', '09121112233', 'Mashhad, Iran', '2023-03-20'),
('Zahra', 'Hosseini', '5566778899', 'pass4', '09125566778', 'Tabriz, Iran', '2023-04-25'),
('Mohammad', 'Jafari', '6677889900', 'pass5', '09126677889', 'Esfahan, Iran', '2023-05-30'),
('Elham', 'Farhadi', '1029384756', 'pass6', '09121029384', 'Kerman, Iran', '2023-06-10'),
('Parsa', 'Shirazi', '5647382910', 'pass7', '09125647382', 'Tehran, Iran', '2023-07-15'),
('Hamed', 'Ghasemi', '8765432109', 'pass8', '09128765432', 'Qom, Iran', '2023-08-20'),
('Samira', 'Rahmani', '1239874560', 'pass9', '09121239874', 'Ahvaz, Iran', '2023-09-25'),
('Omid', 'Ebrahimi', '9876543210', 'pass10', '09129876543', 'Rasht, Iran', '2023-10-30');

-- 4. وارد کردن داده‌های نمونه برای کارکنان (Staff)
INSERT INTO Staff (first_name, last_name, ID_number, password_hash)
VALUES 
('Hasan', 'Rezai', '6543219870', 'staff1'),
('Mina', 'Nasiri', '5678901234', 'staff2'),
('Alireza', 'Tavakoli', '9870123456', 'staff3'),
('Fatemeh', 'Bahrami', '3210987654', 'staff4'),
('Nima', 'Sadeghi', '7896541230', 'staff5'),
('Shahin', 'Gholami', '4567890123', 'staff6'),
('Elham', 'Shafiei', '2345678901', 'staff7'),
('Ramin', 'Javadi', '8901234567', 'staff8'),
('Mahsa', 'Afshari', '5432109876', 'staff9'),
('Hooman', 'Karami', '6789012345', 'staff10');

-- 5. وارد کردن داده‌های نمونه برای میز امانات (LendingDesk)
INSERT INTO LendingDesk (book_id, reader_id, borrow_date, return_date, remarks)
VALUES 
(1, 1, '2024-01-10', '2024-02-10', 'Returned on time'),
(2, 2, '2024-01-15', '2024-02-15', 'Returned late'),
(3, 3, '2024-02-01', NULL, 'Not yet returned'),
(4, 4, '2024-02-10', '2024-03-10', 'Returned on time'),
(5, 5, '2024-02-20', NULL, 'Lost'),
(6, 6, '2024-03-05', '2024-04-05', 'Returned early'),
(7, 7, '2024-03-10', NULL, 'Not yet returned'),
(8, 8, '2024-03-15', '2024-04-15', 'Returned on time'),
(9, 9, '2024-04-01', NULL, 'Pending return'),
(10, 10, '2024-04-05', '2024-05-05', 'Returned late');

-- 6. وارد کردن داده‌های نمونه برای گزارشات (Reports)
INSERT INTO Reports (reader_id, staff_id, action_type, detail, created_date)
VALUES 
(1, 1, 'borrow', 'Borrowed "To Kill a Mockingbird"', '2024-01-10'),
(2, 2, 'borrow', 'Borrowed "1984"', '2024-01-15'),
(3, 3, 'borrow', 'Borrowed "The Great Gatsby"', '2024-02-01'),
(4, 4, 'borrow', 'Borrowed "Pride and Prejudice"', '2024-02-10'),
(5, 5, 'borrow', 'Borrowed "Moby Dick"', '2024-02-20'),
(6, 6, 'borrow', 'Borrowed "War and Peace"', '2024-03-05'),
(7, 7, 'borrow', 'Borrowed "Harry Potter"', '2024-03-10'),
(8, 8, 'borrow', 'Borrowed "The Hobbit"', '2024-03-15'),
(9, 9, 'borrow', 'Borrowed "Brave New World"', '2024-04-01'),
(10, 10, 'borrow', 'Borrowed "The Catcher in the Rye"', '2024-04-05');
