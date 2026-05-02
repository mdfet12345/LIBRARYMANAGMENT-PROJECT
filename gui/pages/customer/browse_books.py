from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QGridLayout,
    QLineEdit, QComboBox, QHBoxLayout, QLabel
)
from PyQt5.QtCore import Qt

from database.database_manager import DatabaseManager
from gui.components.book_card import BookCard


class BrowseBooksPage(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.db = DatabaseManager()
        self.all_books = []
        self.filtered_books = []

        self.setup_ui()
        self.load_books()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
            }

            QLabel#pageTitle {
                font-size: 28px;
                font-weight: 800;
                color: #1a1a1a;
                background: transparent;
            }

            QLineEdit, QComboBox {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                min-height: 34px;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #2b2b2b;
            }

            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(18)

        title = QLabel("Browse Books")
        title.setObjectName("pageTitle")

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(12)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search by title or author")

        self.category_filter = QComboBox()
        self.category_filter.addItem("ALL")

        self.status_filter = QComboBox()
        self.status_filter.addItems(["ALL", "Available", "Currently Unavailable"])

        filter_layout.addWidget(self.search, 2)
        filter_layout.addWidget(self.category_filter, 1)
        filter_layout.addWidget(self.status_filter, 1)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(18)
        self.grid.setVerticalSpacing(18)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.scroll.setWidget(self.container)

        main_layout.addWidget(title)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.scroll, 1)

        self.search.textChanged.connect(self.apply_filters)
        self.category_filter.currentTextChanged.connect(self.apply_filters)
        self.status_filter.currentTextChanged.connect(self.apply_filters)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.display_books(self.filtered_books)

    def load_books(self):
        self.all_books = self.db.get_all_books()
        self.filtered_books = self.all_books

        categories = sorted(set(book[3] for book in self.all_books))

        self.category_filter.blockSignals(True)
        self.category_filter.clear()
        self.category_filter.addItem("ALL")
        self.category_filter.addItems(categories)
        self.category_filter.blockSignals(False)

        self.display_books(self.filtered_books)

    def clear_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def get_column_count(self):
        viewport_width = self.scroll.viewport().width()
        card_width = 220
        spacing = 18
        
        columns = (viewport_width + spacing) // (card_width + spacing)
        return max(4, columns)

    def display_books(self, books):
        self.clear_grid()

        if not books:
            empty_label = QLabel("No books found")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("""
                QLabel {
                    color: #777777;
                    font-size: 18px;
                    font-style: italic;
                    background: transparent;
                }
            """)
            self.grid.addWidget(empty_label, 0, 0)
            return

        max_columns = self.get_column_count()
        
        row = 0
        col = 0

        for book in books:
            card = BookCard(book, self.handle_add_to_cart)
            self.grid.addWidget(card, row, col)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

    def apply_filters(self):
        keyword = self.search.text().strip().lower()
        selected_category = self.category_filter.currentText()
        selected_status = self.status_filter.currentText()

        filtered = []

        for book in self.all_books:
            title = book[1].lower()
            author = book[2].lower()
            category = book[3]
            available_copies = book[6]

            matches_keyword = keyword in title or keyword in author
            matches_category = selected_category == "ALL" or category == selected_category

            if selected_status == "ALL":
                matches_status = True
            elif selected_status == "Available":
                matches_status = available_copies > 0
            else:
                matches_status = available_copies == 0

            if matches_keyword and matches_category and matches_status:
                filtered.append(book)

        self.filtered_books = filtered
        self.display_books(self.filtered_books)
        
        
    def handle_add_to_cart(self, book_id):
        from functions.cart_functions import add_book_to_cart
        from functions.ui_messages import show_info, show_error

        try:
            user = self.main_window.current_user

            if not user:
                show_error(self, "Error", "No user is currently logged in")
                return

            if isinstance(user, dict):
                user_id = user.get("id") or user.get("user_id")
            else:
                user_id = user[0]

            if not user_id:
                show_error(self, "Error", "Could not find current user ID")
                return

            conn = self.db.connect()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT fine_amount FROM users WHERE id = ?",
                (user_id,)
            )

            result = cursor.fetchone()
            conn.close()

            fine_amount = result[0] if result and result[0] is not None else 0

            if float(fine_amount) > 0:
                show_error(
                    self,
                    "Borrowing Blocked",
                    f"You cannot borrow books until you pay your fine of ${fine_amount}"
                )
                return

            success, message = add_book_to_cart(user, book_id)

            if success:
                show_info(self, "Cart", message)
            else:
                show_error(self, "Cart", message)

        except Exception as e:
            show_error(self, "Crash Error", str(e))