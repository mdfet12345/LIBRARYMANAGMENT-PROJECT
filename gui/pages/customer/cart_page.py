from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea,
    QFrame, QHBoxLayout, QPushButton, QSpinBox
)
from PyQt5.QtCore import Qt

from database.database_manager import DatabaseManager
from functions.ui_messages import show_info, show_error, show_confirm
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap

class CartPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
            }

            QLabel#title {
                font-size: 28px;
                font-weight: 800;
                color: #1a1a1a;
                background: transparent;
            }

            QFrame#cartItem {
                background-color: white;
                border-radius: 14px;
                border: 1px solid #eeeeee;
            }

            QLabel {
                background: transparent;
            }

            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }

            QSpinBox {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 6px;
                padding: 6px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(18)

        title = QLabel("My Cart")
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

        self.borrow_btn = QPushButton("Borrow Books")
        self.borrow_btn.clicked.connect(self.borrow_books)

        main_layout.addWidget(title)
        main_layout.addWidget(self.scroll, 1)
        main_layout.addWidget(self.borrow_btn)

    def load_cart(self):
        self.clear_items()

        user = self.main_window.current_user
        if not user:
            return

        items = self.db.get_cart_items(user["id"])

        if not items:
            empty = QLabel("Your cart is empty.")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("font-size: 18px; color: #777; font-style: italic;")
            self.items_layout.addWidget(empty)
            self.borrow_btn.setEnabled(False)
            return

        self.borrow_btn.setEnabled(True)

        for item in items:
            self.items_layout.addWidget(self.create_cart_item(item))
        self.items_layout.addStretch()

    def clear_items(self):
        while self.items_layout.count():
            item = self.items_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def create_cart_item(self, item):
        cart_id = item[0]
        title = item[2]
        author = item[3]
        category = item[4]
        pages = item[5]
        image_path = item[6]
        borrow_days = item[7]

        frame = QFrame()
        frame.setObjectName("cartItem")
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

        details.addWidget(title_label)
        details.addWidget(meta_label)
        details.addWidget(pages_label)
        details.addStretch()

        days_spinner = QSpinBox()
        days_spinner.setRange(1, 14)
        days_spinner.setValue(borrow_days)
        days_spinner.setPrefix("Days: ")
        days_spinner.setFixedWidth(150)
        days_spinner.setMinimumHeight(36)

        days_spinner.valueChanged.connect(
            lambda value: self.db.update_cart_borrow_days(cart_id, value)
        )

        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda: self.remove_item(cart_id))

        right_side = QVBoxLayout()
        right_side.addWidget(days_spinner)
        right_side.addStretch()
        right_side.addWidget(remove_btn)

        layout.addWidget(image)
        layout.addLayout(details, 1)
        layout.addLayout(right_side)

        return frame

    def remove_item(self, cart_id):
        try:
            self.db.remove_from_cart(cart_id)
            self.load_cart()
        except Exception as e:
            from functions.ui_messages import show_error
            show_error(self, "Error", f"Could not remove item:\n{str(e)}")
    def borrow_books(self):
        from functions.ui_messages import show_info, show_error, show_confirm
        from PyQt5.QtWidgets import QMessageBox

        try:
            user = self.main_window.current_user

            if not user:
                show_error(self, "Error", "Please login first.")
                return

            confirm = show_confirm(
                self,
                "Confirm Borrow",
                "Are you sure you want to borrow the books in your cart?"
            )

            if confirm != QMessageBox.Yes:
                return

            success, message = self.db.checkout_cart(user["id"])

            if success:
                show_info(self, "Success", message)
                self.load_cart()
            else:
                show_error(self, "Error", message)

        except Exception as e:
            show_error(self, "Checkout Error", str(e))