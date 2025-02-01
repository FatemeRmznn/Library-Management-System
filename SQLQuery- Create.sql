IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'Library_Management')
CREATE DATABASE Library_Management;
GO

USE Library_Management;
GO

CREATE TABLE Publishers (
  publisher_id INT IDENTITY (1,1) PRIMARY KEY,
  publisher_name VARCHAR(255) NOT NULL,
  [address] VARCHAR(255) ,
  established_year INT CHECK (established_year >= 1000 AND established_year <= YEAR(GETDATE())),
  contact_number VARCHAR(20) NOT NULL
);
GO

CREATE TABLE Books (
  book_id INT IDENTITY (1,1) PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255) NOT NULL,
  publisher_id INT NOT NULL,
  publication_year INT CHECK (publication_year >= 1000 AND publication_year <= YEAR(GETDATE())),
  available BIT DEFAULT 1,  -- 1 = موجود، 0 = ناموجود
  category VARCHAR(255),
  details TEXT,
  FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id) ON DELETE CASCADE
);
GO

CREATE TABLE Readers (
  reader_id INT IDENTITY (1,1) PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  ID_number VARCHAR(10) UNIQUE NOT NULL,
  password_hash NVARCHAR(255) NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  [address] VARCHAR(255),
  registration_date DATE DEFAULT GETDATE()
);
GO

CREATE TABLE Staff (
  staff_id INT IDENTITY (1,1) PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  ID_number VARCHAR(10) UNIQUE NOT NULL,
  password_hash NVARCHAR(255) NOT NULL
);
GO

CREATE TABLE LendingDesk (
  lending_id INT IDENTITY (1,1) PRIMARY KEY,
  book_id INT NOT NULL,
  reader_id INT NOT NULL,
  borrow_date DATE DEFAULT GETDATE(),
  return_date DATE,
  remarks VARCHAR(255),
  FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE,
  FOREIGN KEY (reader_id) REFERENCES Readers(reader_id) ON DELETE CASCADE
);
GO

CREATE TABLE Reports (
  report_id INT IDENTITY (1,1) PRIMARY KEY,
  reader_id INT NOT NULL,   -- شخصی که کتاب رو گرفته یا پس داده
  staff_id INT NULL,        -- مسئول کتابخانه که اطلاعات رو ثبت کرده (NULLABLE)
  action_type VARCHAR(10) CHECK (action_type IN ('borrow', 'return')),  -- نوع عملیات
  detail TEXT NOT NULL,
  created_date DATE DEFAULT GETDATE(),
  FOREIGN KEY (reader_id) REFERENCES Readers(reader_id) ON DELETE CASCADE,
  FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE SET NULL
);
