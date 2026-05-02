import sqlite3
from database.db_config import DB_PATH

class DatabaseManager:
    def __init__(self):
        self.db_path = DB_PATH

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # user functions

    def register_user(self, name, username, national_id, age, email, password):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users (
                    name, username, national_id, age, email, password
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, username, national_id, age, email, password))

            conn.commit()
            conn.close()
            return True

        except sqlite3.IntegrityError as e:
            print("register integrity error:", e)
            return False

        except Exception as e:
            print("register error:", e)
            return False

    def login_user(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                username,
                national_id,
                age,
                email,
                password,
                is_verified,
                fine_amount,
                created_at
            FROM users
            WHERE username = ?
            AND password = ?
        """, (username, password))

        user = cursor.fetchone()
        conn.close()
        return user

    def login_librarian(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM librarian
            WHERE username = ? AND password = ?
        """, (username, password))

        librarian = cursor.fetchone()
        conn.close()
        return librarian

    def verify_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET is_verified = 1
            WHERE id = ?
        """, (user_id,))

        conn.commit()
        conn.close()

    def unverify_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET is_verified = 0
            WHERE id = ?
        """, (user_id,))

        conn.commit()
        conn.close()

    def clear_fines(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET fine_amount = 0
            WHERE id = ?
        """, (user_id,))

        conn.commit()
        conn.close()

    def get_user_fines(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT fine_amount
            FROM users
            WHERE id = ?
        """, (user_id,))

        result = cursor.fetchone()
        conn.close()

        return result[0] if result and result[0] is not None else 0

    def delete_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM borrowed_books
            WHERE user_id = ?
            AND status = 'borrowed'
        """, (user_id,))

        borrowed_count = cursor.fetchone()[0]

        if borrowed_count > 0:
            conn.close()
            return False, "This member cannot be deleted because they are currently borrowing a book."

        cursor.execute("""
            DELETE FROM users
            WHERE id = ?
        """, (user_id,))

        conn.commit()
        conn.close()

        return True, "Member deleted successfully"

    def get_all_users(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                username,
                national_id,
                age,
                email,
                password,
                is_verified,
                fine_amount,
                created_at
            FROM users
            ORDER BY created_at DESC
        """)

        users = cursor.fetchall()
        conn.close()
        return users

    # book functions

    def add_book(self, title, author, category, pages, copies, image_path=None):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO books
            (title, author, category, pages, copies, available_copies, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            title,
            author,
            category,
            pages,
            copies,
            copies,
            image_path
        ))

        conn.commit()
        conn.close()

    def get_all_books(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM books
            ORDER BY id DESC
        """)

        books = cursor.fetchall()
        conn.close()
        return books

    def delete_book(self, book_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM borrowed_books
            WHERE book_id = ?
            AND status = 'borrowed'
        """, (book_id,))

        borrowed_count = cursor.fetchone()[0]

        if borrowed_count > 0:
            conn.close()
            return False, "This book cannot be deleted because it is currently borrowed by a member."

        cursor.execute("""
            DELETE FROM books
            WHERE id = ?
        """, (book_id,))

        conn.commit()
        conn.close()

        return True, "Book deleted successfully"

    def update_book(self, book_id, title, author, category, pages, copies, image_path=None):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT copies, available_copies
            FROM books
            WHERE id = ?
        """, (book_id,))

        result = cursor.fetchone()

        if not result:
            conn.close()
            return False, "Book not found"

        old_copies, old_available = result
        difference = copies - old_copies
        new_available = old_available + difference

        if new_available < 0:
            conn.close()
            return False, "Copies cannot be less than currently borrowed copies"

        cursor.execute("""
            UPDATE books
            SET title = ?,
                author = ?,
                category = ?,
                pages = ?,
                copies = ?,
                available_copies = ?,
                image_path = ?
            WHERE id = ?
        """, (
            title,
            author,
            category,
            pages,
            copies,
            new_available,
            image_path,
            book_id
        ))

        conn.commit()
        conn.close()

        return True, "Book updated successfully"

    # cart functions

    def get_cart_count(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM cart
            WHERE user_id = ?
        """, (user_id,))

        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_borrowed_count(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM borrowed_books
            WHERE user_id = ?
            AND status = 'borrowed'
        """, (user_id,))

        count = cursor.fetchone()[0]
        conn.close()
        return count

    def is_book_in_cart(self, user_id, book_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM cart
            WHERE user_id = ?
            AND book_id = ?
        """, (user_id, book_id))

        result = cursor.fetchone()
        conn.close()

        return result is not None

    def add_to_cart(self, user_id, book_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT is_verified, fine_amount
            FROM users
            WHERE id = ?
        """, (user_id,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return False, "User not found"

        is_verified = user[0]
        fine_amount = user[1] if user[1] is not None else 0

        if is_verified == 0:
            conn.close()
            return False, "You aren't verified yet.\nPlease wait for the librarian to verify you."

        if fine_amount > 0:
            conn.close()
            return False, f"You cannot borrow books until you pay your fine of ${fine_amount}"

        cursor.execute("""
            SELECT COUNT(*)
            FROM borrowed_books
            WHERE user_id = ?
            AND status = 'borrowed'
            AND return_date < DATE('now')
        """, (user_id,))
        overdue_count = cursor.fetchone()[0]

        if overdue_count > 0:
            conn.close()
            return False, "You cannot borrow another book because you currently have an overdue book."

        cursor.execute("""
            SELECT available_copies
            FROM books
            WHERE id = ?
        """, (book_id,))
        book = cursor.fetchone()

        if not book:
            conn.close()
            return False, "Book not found"

        if book[0] <= 0:
            conn.close()
            return False, "This book is currently out of stock"

        cursor.execute("""
            SELECT id
            FROM cart
            WHERE user_id = ?
            AND book_id = ?
        """, (user_id, book_id))

        if cursor.fetchone():
            conn.close()
            return False, "This book is already in your cart"

        cursor.execute("""
            SELECT id
            FROM borrowed_books
            WHERE user_id = ?
            AND book_id = ?
            AND status = 'borrowed'
        """, (user_id, book_id))

        if cursor.fetchone():
            conn.close()
            return False, "You already borrowed this book"

        cursor.execute("""
            SELECT COUNT(*)
            FROM cart
            WHERE user_id = ?
        """, (user_id,))
        cart_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM borrowed_books
            WHERE user_id = ?
            AND status = 'borrowed'
        """, (user_id,))
        borrowed_count = cursor.fetchone()[0]

        if cart_count + borrowed_count >= 3:
            conn.close()
            return False, "You can only have 3 books at a time"

        cursor.execute("""
            INSERT INTO cart (user_id, book_id, borrow_days)
            VALUES (?, ?, ?)
        """, (user_id, book_id, 3))

        conn.commit()
        conn.close()

        return True, "Book added to cart"

    def get_cart_items(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                cart.id,
                books.id,
                books.title,
                books.author,
                books.category,
                books.pages,
                books.image_path,
                cart.borrow_days
            FROM cart
            JOIN books ON cart.book_id = books.id
            WHERE cart.user_id = ?
            ORDER BY cart.id DESC
        """, (user_id,))

        items = cursor.fetchall()
        conn.close()

        return items

    def remove_from_cart(self, cart_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM cart
            WHERE id = ?
        """, (cart_id,))

        conn.commit()
        conn.close()

    def update_cart_borrow_days(self, cart_id, borrow_days):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE cart
            SET borrow_days = ?
            WHERE id = ?
        """, (borrow_days, cart_id))

        conn.commit()
        conn.close()

    def checkout_cart(self, user_id):
        from datetime import date, timedelta

        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT fine_amount
                FROM users
                WHERE id = ?
            """, (user_id,))
            fine_result = cursor.fetchone()

            if not fine_result:
                conn.close()
                return False, "User not found"

            fine_amount = fine_result[0] if fine_result[0] is not None else 0

            if fine_amount > 0:
                conn.close()
                return False, f"You cannot borrow books until you pay your fine of ${fine_amount}"

            cursor.execute("""
                SELECT COUNT(*)
                FROM borrowed_books
                WHERE user_id = ?
                AND status = 'borrowed'
                AND return_date < DATE('now')
            """, (user_id,))
            overdue_count = cursor.fetchone()[0]

            if overdue_count > 0:
                conn.close()
                return False, "You cannot checkout because you currently have an overdue book."

            cursor.execute("""
                SELECT cart.id, cart.book_id, cart.borrow_days, books.available_copies
                FROM cart
                JOIN books ON cart.book_id = books.id
                WHERE cart.user_id = ?
            """, (user_id,))
            cart_items = cursor.fetchall()

            if not cart_items:
                conn.close()
                return False, "Your cart is empty"

            borrow_date = date.today()

            for cart_id, book_id, borrow_days, available_copies in cart_items:
                if available_copies <= 0:
                    conn.close()
                    return False, "One of the books is no longer available"

                return_date = borrow_date + timedelta(days=borrow_days)

                cursor.execute("""
                    INSERT INTO borrowed_books 
                    (user_id, book_id, borrow_date, return_date, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id,
                    book_id,
                    borrow_date.isoformat(),
                    return_date.isoformat(),
                    "borrowed"
                ))

                cursor.execute("""
                    UPDATE books
                    SET available_copies = available_copies - 1
                    WHERE id = ?
                """, (book_id,))

            cursor.execute("""
                DELETE FROM cart
                WHERE user_id = ?
            """, (user_id,))

            conn.commit()
            conn.close()

            return True, "Books borrowed successfully"

        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)

    # message functions

    def send_message(self, sender_type, sender_id, receiver_type, receiver_id, subject, message):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages
            (sender_type, sender_id, receiver_type, receiver_id, subject, message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            sender_type,
            sender_id,
            receiver_type,
            receiver_id,
            subject,
            message
        ))

        conn.commit()
        conn.close()

    def get_messages_for_user(self, receiver_type, receiver_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM messages
            WHERE receiver_type = ?
            AND receiver_id = ?
            AND is_read = 0
            ORDER BY created_at DESC
        """, (receiver_type, receiver_id))

        messages = cursor.fetchall()
        conn.close()
        return messages

    def mark_message_as_read(self, message_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE messages
            SET is_read = 1
            WHERE id = ?
        """, (message_id,))

        conn.commit()
        conn.close()

    def delete_message(self, message_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM messages
            WHERE id = ?
        """, (message_id,))

        conn.commit()
        conn.close()

    # personal books / returns

    def get_personal_books(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                borrowed_books.id,
                books.title,
                books.author,
                books.category,
                books.pages,
                books.image_path,
                borrowed_books.return_date,
                CASE
                    WHEN return_requests.id IS NOT NULL THEN 1
                    ELSE 0
                END AS has_pending_return
            FROM borrowed_books
            JOIN books ON borrowed_books.book_id = books.id
            LEFT JOIN return_requests
                ON return_requests.borrow_id = borrowed_books.id
                AND return_requests.status = 'pending'
            WHERE borrowed_books.user_id = ?
            AND borrowed_books.status = 'borrowed'
            ORDER BY borrowed_books.return_date ASC
        """, (user_id,))

        books = cursor.fetchall()
        conn.close()
        return books

    def create_return_request(self, borrow_id):
        from datetime import date

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM return_requests
            WHERE borrow_id = ?
            AND status = 'pending'
        """, (borrow_id,))

        existing_request = cursor.fetchone()

        if existing_request:
            conn.close()
            return False, "Return request already exists"

        cursor.execute("""
            INSERT INTO return_requests
            (borrow_id, request_date, status)
            VALUES (?, ?, ?)
        """, (
            borrow_id,
            date.today().isoformat(),
            "pending"
        ))

        conn.commit()
        conn.close()

        return True, "Return request created"

    def get_pending_return_requests(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                return_requests.id,
                users.name,
                books.title,
                borrowed_books.borrow_date,
                borrowed_books.return_date,
                borrowed_books.id
            FROM return_requests
            JOIN borrowed_books ON return_requests.borrow_id = borrowed_books.id
            JOIN users ON borrowed_books.user_id = users.id
            JOIN books ON borrowed_books.book_id = books.id
            WHERE return_requests.status = 'pending'
            ORDER BY return_requests.request_date ASC
        """)

        requests = cursor.fetchall()
        conn.close()

        return requests

    def approve_return(self, return_request_id, condition):
        from datetime import date

        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT borrowed_books.id, borrowed_books.return_date, borrowed_books.book_id, borrowed_books.user_id
                FROM return_requests
                JOIN borrowed_books ON return_requests.borrow_id = borrowed_books.id
                WHERE return_requests.id = ?
            """, (return_request_id,))

            data = cursor.fetchone()

            if not data:
                conn.close()
                return False, "invalid request"

            borrow_id, return_date, book_id, user_id = data

            today = date.today()
            delay_days = (today - date.fromisoformat(return_date)).days
            delay_days = max(0, delay_days)

            condition_fines = {
                "Excellent": 0,
                "Good": 2,
                "Bad": 5,
                "Damaged": 10
            }

            fine = condition_fines.get(condition, 0)
            delay_fine = delay_days * 5
            fine += delay_fine

            if fine > 0:
                cursor.execute("""
                    UPDATE users
                    SET fine_amount = fine_amount + ?
                    WHERE id = ?
                """, (fine, user_id))

            cursor.execute("""
                UPDATE borrowed_books
                SET status = 'returned'
                WHERE id = ?
            """, (borrow_id,))

            cursor.execute("""
                UPDATE books
                SET available_copies = available_copies + 1
                WHERE id = ?
            """, (book_id,))

            cursor.execute("""
                UPDATE return_requests
                SET status = 'approved',
                    book_condition = ?,
                    fine_amount = ?
                WHERE id = ?
            """, (condition, fine, return_request_id))

            conn.commit()
            conn.close()

            return True, fine

        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)

    # dashboard / librarian

    def get_librarian_dashboard_stats(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM books")
        total_books = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM users")
        total_members = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM borrowed_books
            WHERE status = 'borrowed'
        """)
        borrowed_books = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM borrowed_books
            WHERE status = 'borrowed'
            AND return_date < DATE('now')
        """)
        overdue_books = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM return_requests
            WHERE status = 'pending'
        """)
        pending_returns = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE is_verified = 0
        """)
        unverified_members = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM book_requests")
        book_requests = cursor.fetchone()[0]

        conn.close()

        return {
            "total_books": total_books,
            "total_members": total_members,
            "borrowed_books": borrowed_books,
            "overdue_books": overdue_books,
            "pending_returns": pending_returns,
            "unverified_members": unverified_members,
            "book_requests": book_requests
        }

    def get_all_borrowed_books(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                borrowed_books.id,
                users.name,
                users.username,
                books.title,
                borrowed_books.borrow_date,
                borrowed_books.return_date,
                CASE
                    WHEN borrowed_books.return_date < DATE('now') THEN 'Overdue'
                    ELSE 'On Time'
                END AS return_status
            FROM borrowed_books
            JOIN users ON borrowed_books.user_id = users.id
            JOIN books ON borrowed_books.book_id = books.id
            WHERE borrowed_books.status = 'borrowed'
            ORDER BY borrowed_books.borrow_date DESC
        """)

        records = cursor.fetchall()
        conn.close()
        return records

    # =========================
    # BOOK REQUESTS
    # =========================

    def create_book_request(self, user_id, title, author, notes):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO book_requests (user_id, book_title, author_name, notes)
            VALUES (?, ?, ?, ?)
        """, (user_id, title, author, notes))

        conn.commit()
        conn.close()

    def get_book_requests(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                book_requests.id,
                users.id,
                users.name,
                book_requests.book_title,
                book_requests.author_name,
                book_requests.notes,
                book_requests.created_at
            FROM book_requests
            JOIN users ON book_requests.user_id = users.id
            ORDER BY book_requests.created_at DESC
        """)

        data = cursor.fetchall()
        conn.close()
        return data

    def delete_book_request(self, request_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM book_requests
            WHERE id = ?
        """, (request_id,))

        conn.commit()
        conn.close()

    def get_request_replies_for_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, subject, message, created_at
            FROM messages
            WHERE receiver_type = 'user'
            AND receiver_id = ?
            AND sender_type = 'librarian'
            ORDER BY created_at DESC
        """, (user_id,))

        replies = cursor.fetchall()
        conn.close()
        return replies