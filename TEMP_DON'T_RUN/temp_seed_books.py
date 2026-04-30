from database.database_manager import DatabaseManager

db = DatabaseManager()

# -------------------------
# CLEAR OLD BOOKS
# -------------------------
conn = db.connect()
cursor = conn.cursor()
cursor.execute("DELETE FROM books")
conn.commit()
conn.close()

print("Old books cleared.")

# -------------------------
# NEW BOOKS WITH IMAGES
# -------------------------
books = [
    ("The Great Gatsby", "F. Scott Fitzgerald", "Novel", 180, 5, "assets/books/gatsby.jpg"),
    ("1984", "George Orwell", "Dystopian", 328, 4, "assets/books/1984.jpg"),
    ("The Alchemist", "Paulo Coelho", "Philosophy", 208, 6, "assets/books/alchemist.jpg"),
    ("Sapiens", "Yuval Noah Harari", "History", 498, 3, "assets/books/sapiens.jpg"),
    ("Clean Code", "Robert C. Martin", "Programming", 464, 2, "assets/books/clean_code.jpg"),
    ("Atomic Habits", "James Clear", "Self Development", 320, 5, "assets/books/atomic_habits.jpg"),
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 310, 4, "assets/books/hobbit.jpg"),
    ("Rich Dad Poor Dad", "Robert Kiyosaki", "Finance", 336, 3, "assets/books/rich_dad.jpg"),
    ("To Kill a Mockingbird", "Harper Lee", "Classic", 281, 5, "assets/books/mockingbird.jpg"),
    ("The Psychology of Money", "Morgan Housel", "Finance", 256, 4, "assets/books/psychology_money.jpg"),
]

for book in books:
    db.add_book(
        title=book[0],
        author=book[1],
        category=book[2],
        pages=book[3],
        copies=book[4],
        image_path=book[5]
    )

print("Books with images added successfully!")