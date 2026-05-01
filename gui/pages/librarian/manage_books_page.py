from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout,
    QLineEdit, QComboBox, QHBoxLayout, QFrame, QPushButton,
    QDialog, QFormLayout, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from database.database_manager import DatabaseManager
from functions.ui_messages import show_info, show_error, show_confirm


class ManageBooksPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = DatabaseManager()
        self.all_books = []
        self.filtered_books = []
        self.setup_ui()

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

            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(18)

        title = QLabel("Manage Books")
        title.setObjectName("pageTitle")

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(12)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search by title or author")

        self.category_filter = QComboBox()
        self.category_filter.addItem("ALL")

        self.status_filter = QComboBox()
        self.status_filter.addItems(["ALL", "Available", "Out of Stock"])

        filter_layout.addWidget(self.search, 2)
        filter_layout.addWidget(self.category_filter, 1)
        filter_layout.addWidget(self.status_filter, 1)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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

    def get_column_count(self):
        viewport_width = self.scroll.viewport().width()
        card_width = 215
        spacing = 18
        columns = (viewport_width + spacing) // (card_width + spacing)

        return max(4, columns)

    def clear_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

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
            card = LibrarianBookCard(
                book,
                delete_callback=self.delete_book,
                update_callback=self.update_book
            )

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

    def delete_book(self, book_id):
        confirm = show_confirm(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this book?"
        )

        if confirm != QMessageBox.Yes:
            return

        self.db.delete_book(book_id)
        show_info(self, "Success", "Book deleted successfully")
        self.load_books()

    def update_book(self, book):
        dialog = UpdateBookDialog(self, book)

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            success, message = self.db.update_book(
                book_id=book[0],
                title=data["title"],
                author=data["author"],
                category=data["category"],
                pages=data["pages"],
                copies=data["copies"],
                image_path=data["image_path"]
            )

            if success:
                show_info(self, "Success", message)
                self.load_books()
            else:
                show_error(self, "Error", message)


class LibrarianBookCard(QFrame):
    def __init__(self, book_data, delete_callback, update_callback):
        super().__init__()
        self.book_data = book_data
        self.delete_callback = delete_callback
        self.update_callback = update_callback
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(215, 350)
        self.setObjectName("bookCard")

        self.setStyleSheet("""
            QFrame#bookCard {
                background-color: #ffffff;
                border-radius: 14px;
                border: 1px solid #eeeeee;
            }

            QLabel {
                background: transparent;
                color: #222222;
            }

            QLabel#bookId {
                font-size: 12px;
                color: #777777;
                font-weight: 700;
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

            QLabel#available {
                background-color: #e6f4ea;
                color: #1f8f4d;
                border-radius: 10px;
                padding: 4px 10px;
                font-size: 12px;
                font-weight: 800;
            }

            QLabel#outOfStock {
                background-color: #fdecea;
                color: #c0392b;
                border-radius: 10px;
                padding: 4px 10px;
                font-size: 12px;
                font-weight: 800;
            }

            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }

            QPushButton#deleteBtn {
                background-color: #c0392b;
            }

            QPushButton#deleteBtn:hover {
                background-color: #a93226;
            }
        """)

        book_id = self.book_data[0]
        title = self.book_data[1]
        author = self.book_data[2]
        category = self.book_data[3]
        pages = self.book_data[4]
        copies = self.book_data[5]
        available_copies = self.book_data[6]
        image_path = self.book_data[7]

        is_available = available_copies > 0
        status_text = "Available" if is_available else "Out of Stock"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(7)

        top_row = QHBoxLayout()

        id_label = QLabel(f"#ID_{book_id}")
        id_label.setObjectName("bookId")

        copies_label = QLabel(f"{available_copies}/{copies} copies")
        copies_label.setObjectName("bookMeta")
        copies_label.setAlignment(Qt.AlignRight)

        top_row.addWidget(id_label)
        top_row.addStretch()
        top_row.addWidget(copies_label)

        image_box = QLabel()
        image_box.setAlignment(Qt.AlignCenter)
        image_box.setFixedHeight(100)
        image_box.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border-radius: 10px;
                color: #999999;
                font-size: 12px;
            }
        """)

        if image_path:
            pixmap = QPixmap(image_path)

            if not pixmap.isNull():
                image_box.setPixmap(
                    pixmap.scaled(
                        125, 100,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )
            else:
                image_box.setText("No Image")
        else:
            image_box.setText("No Image")

        title_label = QLabel(title)
        title_label.setObjectName("bookTitle")
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setMinimumHeight(42)

        meta_label = QLabel(f"{author} • {category}")
        meta_label.setObjectName("bookMeta")
        meta_label.setWordWrap(True)
        meta_label.setAlignment(Qt.AlignCenter)

        pages_label = QLabel(f"{pages} pages")
        pages_label.setObjectName("bookMeta")
        pages_label.setAlignment(Qt.AlignCenter)

        status_label = QLabel(status_text)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFixedHeight(26)
        status_label.setObjectName("available" if is_available else "outOfStock")

        button_row = QHBoxLayout()

        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("deleteBtn")

        update_btn = QPushButton("Update")

        delete_btn.clicked.connect(lambda: self.delete_callback(book_id))
        update_btn.clicked.connect(lambda: self.update_callback(self.book_data))

        button_row.addWidget(delete_btn)
        button_row.addWidget(update_btn)

        layout.addLayout(top_row)
        layout.addWidget(image_box)
        layout.addWidget(title_label)
        layout.addWidget(meta_label)
        layout.addWidget(pages_label)
        layout.addWidget(status_label)
        layout.addStretch()
        layout.addLayout(button_row)


class UpdateBookDialog(QDialog):
    def __init__(self, parent, book):
        super().__init__(parent)
        self.book = book
        self.image_path = book[7]
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Update Book")
        self.resize(420, 420)

        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
            }

            QLabel {
                background: transparent;
            }

            QLineEdit, QComboBox {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 6px;
                padding: 8px;
            }

            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 9px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_input = QLineEdit(self.book[1])
        self.author_input = QLineEdit(self.book[2])

        self.category_input = QComboBox()
        self.category_input.addItems([
            "Novel", "Historical", "Religion", "Science", "Technology",
            "Programming", "Fantasy", "Classic", "Finance", "Business",
            "Self Development", "Philosophy", "Biography", "Mystery",
            "Romance", "Poetry", "Education", "Health", "Politics", "Arabic", "Turkish", "Other"
        ])

        index = self.category_input.findText(self.book[3])

        if index >= 0:
            self.category_input.setCurrentIndex(index)

        self.pages_input = QLineEdit(str(self.book[4]))
        self.copies_input = QLineEdit(str(self.book[5]))

        self.image_label = QLabel(self.image_path if self.image_path else "No image selected")
        self.image_label.setWordWrap(True)

        upload_btn = QPushButton("Change Image")
        upload_btn.clicked.connect(self.upload_image)

        form.addRow("Title:", self.title_input)
        form.addRow("Author:", self.author_input)
        form.addRow("Category:", self.category_input)
        form.addRow("Pages:", self.pages_input)
        form.addRow("Copies:", self.copies_input)
        form.addRow("Image:", self.image_label)
        form.addRow("", upload_btn)

        btn_row = QHBoxLayout()

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn.clicked.connect(self.reject)

        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)

        layout.addLayout(form)
        layout.addLayout(btn_row)

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

    def validate_and_accept(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        pages = self.pages_input.text().strip()
        copies = self.copies_input.text().strip()

        if not all([title, author, pages, copies]):
            show_error(self, "Error", "All fields are required")
            return

        if len(title) > 50:
            show_error(self, "Error", "Book title cannot be more than 50 characters")
            return

        if len(author) > 30:
            show_error(self, "Error", "Author name cannot be more than 30 characters.")
            return

        if not pages.isdigit() or int(pages) <= 0:
            show_error(self, "Error", "Pages must be a positive number.")
            return

        if not copies.isdigit() or int(copies) < 0:
            show_error(self, "Error", "Copies must be zero or more.")
            return

        self.accept()

    def get_data(self):
        return {
            "title": self.title_input.text().strip(),
            "author": self.author_input.text().strip(),
            "category": self.category_input.currentText(),
            "pages": int(self.pages_input.text().strip()),
            "copies": int(self.copies_input.text().strip()),
            "image_path": self.image_path
        }