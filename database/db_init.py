from database.db_config import DB_PATH
import sqlite3


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # foreign key
    cursor.execute("PRAGMA foreign_keys = ON")

    # librarian table
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS librarian (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO librarian (id, username, password)
    VALUES (1, 'admin', 'admin123')
    """)

    #  users table
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        national_id TEXT NOT NULL UNIQUE,
        age INTEGER NOT NULL CHECK(age > 0),
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        is_verified INTEGER DEFAULT 0,
        fine_amount REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # books table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT NOT NULL,
        pages INTEGER NOT NULL CHECK(pages > 0),
        copies INTEGER NOT NULL CHECK(copies >= 0),
        available_copies INTEGER NOT NULL CHECK(available_copies >= 0 AND available_copies <= copies),
        image_path TEXT
    )
    """)

    # cart table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        borrow_days INTEGER NOT NULL CHECK(borrow_days BETWEEN 1 AND 14),

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
    )
    """)


    # borrowed books table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrowed_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        borrow_date DATE NOT NULL,
        return_date DATE NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('borrowed', 'returned')),

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
    )
    """)

    # return requests table
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS return_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        borrow_id INTEGER NOT NULL,
        request_date DATE NOT NULL,
        book_condition TEXT,
        fine_amount REAL DEFAULT 0,
        status TEXT NOT NULL CHECK(status IN ('pending', 'approved')),

        FOREIGN KEY (borrow_id) REFERENCES borrowed_books(id) ON DELETE CASCADE
    )
    """)

    # messages table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_type TEXT NOT NULL CHECK(sender_type IN ('librarian', 'user')),
        receiver_type TEXT NOT NULL CHECK(receiver_type IN ('librarian', 'user')),
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        subject TEXT,
        message TEXT NOT NULL,
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    # book requests table
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS book_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_title TEXT NOT NULL,
        author_name TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

    # testing
    print("Database created")


if __name__ == "__main__":
    create_database()