import sqlite3
from database.db_config import DB_PATH


# -------------------------
# LIBRARIAN LOGIN (HARDCODED)
# -------------------------
def check_librarian_login(username, password):
    return username == "admin" and password == "admin123"


# -------------------------
# CUSTOMER LOGIN (DB CHECK)
# -------------------------
def check_customer_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, username, password, is_verified, fine_amount
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "User not found", None

    user_id, name, db_username, db_password, is_verified, fine_amount = user

    if password != db_password:
        return False, "Incorrect password", None

    return True, "Login successful", {
        "id": user_id,
        "name": name,
        "username": db_username,
        "is_verified": is_verified,
        "fine_amount": fine_amount
    }