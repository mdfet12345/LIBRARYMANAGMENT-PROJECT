from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt


class BookCard(QFrame):
    def __init__(self, book_data, add_to_cart_callback=None):
        super().__init__()
        self.book_data = book_data
        self.add_to_cart_callback = add_to_cart_callback
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(220, 320)
        self.setObjectName("bookCard")

        self.setStyleSheet("""
            QFrame#bookCard {
                background-color: #ffffff;
                border-radius: 14px;
                border: 1px solid #eeeeee;
            }

            QLabel {
                background: transparent;
            }

            QLabel#bookTitle {
                font-size: 16px;
                font-weight: 800;
                color: #111111;
            }

            QLabel#bookMeta {
                font-size: 12px;
                color: #666666;
            }

            QLabel#bookStatusAvailable {
                color: #1f8f4d;
                font-size: 12px;
                font-weight: 700;
            }

            QLabel#bookStatusBorrowed {
                color: #c0392b;
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 9px;
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }

            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

        self.book_id = self.book_data[0]
        title = self.book_data[1]
        author = self.book_data[2]
        category = self.book_data[3]
        pages = self.book_data[4]
        available_copies = self.book_data[6]

        is_available = available_copies > 0
        status_text = "Available" if is_available else "Out of stock"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(7)

        from PyQt5.QtGui import QPixmap

        image_box = QLabel()
        image_box.setAlignment(Qt.AlignCenter)
        image_box.setFixedHeight(95)

        image_path = self.book_data[7]

        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                image_box.setPixmap(
                    pixmap.scaled(
                        120, 95,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )
            else:
                image_box.setText("No Image")
        else:
            image_box.setText("No Image")

        image_box.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border-radius: 10px;
                color: #999999;
                font-size: 12px;
            }
        """)
        image_box.setAlignment(Qt.AlignCenter)
        image_box.setFixedHeight(95)
        image_box.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border-radius: 10px;
                color: #999999;
                font-size: 13px;
            }
        """)

        title_label = QLabel(title)
        title_label.setObjectName("bookTitle")
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setMinimumHeight(42)

        meta_line = QLabel(f"{author} • {category}")
        meta_line.setObjectName("bookMeta")
        meta_line.setAlignment(Qt.AlignCenter)
        meta_line.setWordWrap(True)

        pages_label = QLabel(f"{pages} pages")
        pages_label.setObjectName("bookMeta")
        pages_label.setAlignment(Qt.AlignCenter)

        status_label = QLabel(status_text)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setObjectName(
            "bookStatusAvailable" if is_available else "bookStatusBorrowed"
        )

        btn = QPushButton("Add to Cart")
        btn.setEnabled(is_available)
        btn.clicked.connect(self.handle_add_to_cart)

        layout.addWidget(image_box)
        layout.addWidget(title_label)
        layout.addWidget(meta_line)
        layout.addWidget(pages_label)
        layout.addWidget(status_label)
        layout.addStretch()
        layout.addWidget(btn)

    def handle_add_to_cart(self):
        if self.add_to_cart_callback:
            self.add_to_cart_callback(self.book_id)
            
    def shorten_text(text, limit=30):
        return text if len(text) <= limit else text[:limit] + "..."