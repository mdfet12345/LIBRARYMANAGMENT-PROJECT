from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea,
    QFrame, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt

from database.database_manager import DatabaseManager
from functions.ui_messages import show_info, show_error, show_confirm
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap


class PersonalBooksPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #fafafa; }

            QLabel#title {
                font-size: 28px;
                font-weight: 800;
                color: #1a1a1a;
                background: transparent;
            }

            QFrame#bookItem {
                background-color: white;
                border-radius: 14px;
                border: 1px solid #eeeeee;
            }

            QLabel { background: transparent; }

            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: 700;
            }

            QPushButton:hover { background-color: #3a3a3a; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(18)

        title = QLabel("Personal Books")
        title.setObjectName("title")

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.container = QWidget()
        self.items_layout = QVBoxLayout(self.container)
        self.items_layout.setContentsMargins(0, 0, 0, 0)
        self.items_layout.setSpacing(14)
        self.items_layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.container)

        main_layout.addWidget(title)
        main_layout.addWidget(self.scroll, 1)

    def load_books(self):
        self.clear_items()

        user = self.main_window.current_user
        if not user:
            return

        books = self.db.get_personal_books(user["id"])

        if not books:
            empty = QLabel("You don't have any borrowed books.")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: #777777;
                    font-style: italic;
                    background: transparent;
                }
            """)
            self.items_layout.addWidget(empty)
            return

        for book in books:
            self.items_layout.addWidget(self.create_book_item(book))

        self.items_layout.addStretch()

    def clear_items(self):
        while self.items_layout.count():
            item = self.items_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def create_book_item(self, book):
        borrow_id = book[0]
        title = book[1]
        author = book[2]
        category = book[3]
        pages = book[4]
        image_path = book[5]
        return_date = book[6]
        has_pending_return = book[7]
        

        frame = QFrame()
        frame.setObjectName("bookItem")
        frame.setFixedHeight(155)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        image = QLabel()
        image.setFixedSize(100, 120)
        image.setAlignment(Qt.AlignCenter)

        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                image.setPixmap(pixmap.scaled(
                    100, 120,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))
            else:
                image.setText("No Image")
        else:
            image.setText("No Image")

        image.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border-radius: 10px;
                color: #999999;
            }
        """)

        details = QVBoxLayout()
        details.setSpacing(6)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: 800; color: #111;")

        meta_label = QLabel(f"{author} • {category}")
        meta_label.setStyleSheet("font-size: 13px; color: #666;")

        pages_label = QLabel(f"{pages} pages")
        pages_label.setStyleSheet("font-size: 13px; color: #666;")

        return_label = QLabel(f"Last return date: {return_date}")
        return_label.setStyleSheet("font-size: 13px; color: #c0392b; font-weight: 700;")

        details.addWidget(title_label)
        details.addWidget(meta_label)
        details.addWidget(pages_label)
        details.addWidget(return_label)
        details.addStretch()

        return_btn = QPushButton("Waiting approval" if has_pending_return else "Return Book")

        if has_pending_return:
            return_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f58d42;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: 700;
                }
            """)
        else:
            return_btn.clicked.connect(lambda: self.request_return(borrow_id, title))

        layout.addWidget(image)
        layout.addLayout(details, 1)
        layout.addWidget(return_btn)

        return frame

    def request_return(self, borrow_id, title):
        confirm = show_confirm(
            self,
            "Confirm Return",
            f'Are you sure you want to return "{title}"?'
        )

        if confirm != QMessageBox.Yes:
            return

        success, message = self.db.create_return_request(borrow_id)

        if success:
            show_info(
                self,
                "Return Request Created",
                "Return request is created successfully.\nThe librarian will check the book condition to confirm it."
            )
            self.load_books()
        else:
            show_error(self, "Error", message)