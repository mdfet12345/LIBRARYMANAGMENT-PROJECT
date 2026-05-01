import sqlite3
import os

# DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database", "library.db")

print("Using database:", db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# check table if exists
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
    is_kicked INTEGER DEFAULT 0,
    fine_amount REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# seed data
users = [
    ("Emre Yılmaz", "emre", "12345678901", 27, "emre@example.com", "Emre12345", 1),
    ("Zeynep Kaya", "zeynep", "23456789012", 24, "zeynep@example.com", "Zeynep12345", 1),
    ("Ahmet Demir", "ahmet", "34567890123", 31, "ahmet@example.com", "Ahmet12345", 0),
    ("Elif Şahin", "elif", "45678901234", 22, "elif@example.com", "Elif12345", 0),
    ("Can Arslan", "can", "56789012345", 29, "can@example.com", "Can12345", 0),
    ("Merve Çelik", "merve", "67890123456", 26, "merve@example.com", "Merve12345", 1),
    ("Burak Koç", "burak", "78901234567", 34, "burak@example.com", "Burak12345", 0),
]

# add new users
for user in users:
    try:
        cursor.execute("""
            INSERT INTO users (
                name, username, national_id, age, email, password, is_verified
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, user)

        print(f"Added user: {user[1]}")

    except sqlite3.IntegrityError:
        print(f"Skipped existing user: {user[1]}")

conn.commit()
conn.close()

print("seeding finished")