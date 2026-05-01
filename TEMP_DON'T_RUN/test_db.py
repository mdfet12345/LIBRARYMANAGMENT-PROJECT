from database.database_manager import DatabaseManager

db = DatabaseManager()

# testing the add a book
db.add_book(
    title="Test Book",
    author="John Doe",
    category="Novel",
    pages=100,
    copies=5,
    available_copies=5,
    image_path=None,
    availability_status="Available"
)

# testing the get books
books = db.get_all_books()
print(books)

# testing the register user
result = db.register_user(
    "Test User",
    "testuser",
    20,
    "test@email.com",
    "1234"
)

print("User registered:", result)