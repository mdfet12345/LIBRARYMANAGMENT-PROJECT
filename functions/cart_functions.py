from database.database_manager import DatabaseManager


db = DatabaseManager()


def add_book_to_cart(user, book_id):
    if not user:
        return False, "Please login first."

    if user["is_verified"] == 0:
        return False, "You aren't verified yet.\nPlease wait for the librarian to verify you."

    return db.add_to_cart(user["id"], book_id)