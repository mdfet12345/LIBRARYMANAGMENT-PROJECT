from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFileDialog, QFrame
)
from PyQt5.QtCore import Qt

from database.database_manager import DatabaseManager
from functions.ui_messages import show_info, show_error


class AddBookPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = DatabaseManager()
        self.image_path = None
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

            QFrame#formCard {
                background-color: white;
                border-radius: 14px;
                border: 1px solid #eeeeee;
            }

            QLabel {
                background: transparent;
                font-size: 13px;
                color: #555555;
            }

            QLineEdit, QComboBox {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                min-height: 34px;
            }

            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 11px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(18)

        title = QLabel("Add Book")
        title.setObjectName("title")

        card = QFrame()
        card.setObjectName("formCard")
        card.setMaximumWidth(650)

        form = QVBoxLayout(card)
        form.setContentsMargins(28, 28, 28, 28)
        form.setSpacing(12)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Book title")

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author")

        self.category_input = QComboBox()
        self.category_input.addItems([
            "Novel", "Historical", "Religion", "Science", "Technology",
            "Programming", "Fantasy", "Classic", "Finance", "Business",
            "Self Development", "Philosophy", "Biography", "Mystery",
            "Romance", "Poetry", "Education", "Health", "Politics", "ِArabic", "Turkish", "Other"
        ])

        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("Pages")

        self.copies_input = QLineEdit()
        self.copies_input.setPlaceholderText("Copies")

        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)

        upload_btn = QPushButton("Upload Image")
        add_btn = QPushButton("Add Book")

        form.addWidget(QLabel("Title"))
        form.addWidget(self.title_input)
        form.addWidget(QLabel("Author"))
        form.addWidget(self.author_input)
        form.addWidget(QLabel("Category"))
        form.addWidget(self.category_input)
        form.addWidget(QLabel("Pages"))
        form.addWidget(self.pages_input)
        form.addWidget(QLabel("Copies"))
        form.addWidget(self.copies_input)
        form.addWidget(self.image_label)
        form.addWidget(upload_btn)
        form.addWidget(add_btn)

        main_layout.addWidget(title)
        main_layout.addWidget(card, alignment=Qt.AlignTop)
        main_layout.addStretch()

        upload_btn.clicked.connect(self.upload_image)
        add_btn.clicked.connect(self.add_book)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Book Image",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if file_path:
            self.image_path = file_path
            self.image_label.setText(file_path)

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        category = self.category_input.currentText()
        pages = self.pages_input.text().strip()
        copies = self.copies_input.text().strip()
        
        if len(title) > 50:
            show_error(self, "Error", "Book title cannot be more than 50 characters")
            return
        
        if len(author) > 30:
            show_error(self, "Error", "Author name cannot be more than 30 characters")
            return

        if not all([title, author, pages, copies]):
            show_error(self, "Error", "All fields are required")
            return

        if not pages.isdigit() or int(pages) <= 0:
            show_error(self, "Error", "Pages must be a positive number")
            return

        if not copies.isdigit() or int(copies) <= 0:
            show_error(self, "Error", "Copies must be a positive number")
            return

        self.db.add_book(
            title=title,
            author=author,
            category=category,
            pages=int(pages),
            copies=int(copies),
            image_path=self.image_path
        )

        show_info(self, "Success", "Book added successfully")
        self.clear_fields()

    def clear_fields(self):
        self.title_input.clear()
        self.author_input.clear()
        self.pages_input.clear()
        self.copies_input.clear()
        self.category_input.setCurrentIndex(0)
        self.image_path = None
        self.image_label.setText("No image selected")