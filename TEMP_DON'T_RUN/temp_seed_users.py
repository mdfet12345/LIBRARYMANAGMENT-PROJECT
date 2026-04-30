from database.database_manager import DatabaseManager

db = DatabaseManager()

users = [
    ("Ali Hassan", "ali", 22, "ali@example.com", "Ali12345", 1),
    ("Sara Ahmed", "sara", 25, "sara@example.com", "Sara12345", 0),
    ("Omar Khaled", "omar", 30, "omar@example.com", "Omar12345", 0),
    ("Mona Saleh", "mona", 21, "mona@example.com", "Mona12345", 0),
    ("Yousef Nader", "yousef", 28, "yousef@example.com", "Yousef12345", 0),
]

for name, username, age, email, password, verified in users:
    success = db.register_user(name, username, age, email, password)

    if success:
        print(f"Added user: {username}")
    else:
        print(f"Skipped existing user: {username}")

    if verified == 1:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET is_verified = 1
            WHERE username = ?
        """, (username,))
        conn.commit()
        conn.close()
        print(f"Verified user: {username}")

print("User seeding finished.")