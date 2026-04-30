from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QTextEdit,
    QHBoxLayout
)
from PyQt5.QtCore import Qt

from database.database_manager import DatabaseManager
from functions.ui_messages import show_info, show_error, show_confirm
from PyQt5.QtWidgets import QMessageBox


class LibrarianMessagesPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = DatabaseManager()

        self.requests = []
        self.selected_request_id = None
        self.selected_request_user_id = None

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

            QLabel {
                background: transparent;
            }

            QTableWidget {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #eeeeee;
                gridline-color: #eeeeee;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #2b2b2b;
                color: white;
                padding: 8px;
                border: none;
                font-weight: 700;
            }

            QTextEdit {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        title = QLabel("Book Requests")
        title.setObjectName("title")

        self.requests_table = QTableWidget()
        self.requests_table.setColumnCount(5)
        self.requests_table.setHorizontalHeaderLabels(
            ["Customer", "Book Title", "Author", "Notes Preview", "Date"]
        )
        self.requests_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.requests_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.requests_table.cellClicked.connect(self.show_request_details)

        self.request_view = QTextEdit()
        self.request_view.setReadOnly(True)
        self.request_view.setPlaceholderText("Select a book request to read details...")

        self.reply_input = QTextEdit()
        self.reply_input.setPlaceholderText("Write a reply to the selected request...")
        self.reply_input.setFixedHeight(100)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.delete_request_btn = QPushButton("Delete Request")
        self.delete_request_btn.setObjectName("deleteBtn")

        self.reply_request_btn = QPushButton("Send Reply")

        self.delete_request_btn.clicked.connect(self.delete_selected_request)
        self.reply_request_btn.clicked.connect(self.reply_to_selected_request)

        button_layout.addWidget(self.delete_request_btn)
        button_layout.addWidget(self.reply_request_btn)

        layout.addWidget(title)
        layout.addWidget(self.requests_table, 2)
        layout.addWidget(self.request_view, 1)
        layout.addWidget(self.reply_input)
        layout.addLayout(button_layout)

    def load_messages(self):
        self.load_requests()

    def load_requests(self):
        self.requests = self.db.get_book_requests()

        self.selected_request_id = None
        self.selected_request_user_id = None
        self.request_view.clear()
        self.reply_input.clear()

        self.requests_table.setRowCount(0)

        for row, req in enumerate(self.requests):
            self.requests_table.insertRow(row)

            customer_name = req[2]
            book_title = req[3]
            author = req[4] or ""
            notes = req[5] or ""
            date = req[6]

            preview_notes = notes[:45] + "..." if len(notes) > 45 else notes

            row_data = [
                customer_name,
                book_title,
                author,
                preview_notes,
                date
            ]

            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.requests_table.setItem(row, col, item)

        self.requests_table.resizeColumnsToContents()

    def show_request_details(self, row, col):
        req = self.requests[row]

        self.selected_request_id = req[0]
        self.selected_request_user_id = req[1]

        customer_name = req[2]
        book_title = req[3]
        author = req[4] or "Not provided"
        notes = req[5] or "No notes"
        date = req[6]

        self.request_view.setText(
            f"Customer: {customer_name}\n"
            f"Book: {book_title}\n"
            f"Author: {author}\n"
            f"Date: {date}\n\n"
            f"Notes:\n{notes}"
        )

        self.reply_input.setText(f"About your request for '{book_title}': ")

    def reply_to_selected_request(self):
        if not self.selected_request_id or not self.selected_request_user_id:
            show_error(self, "Error", "Select a book request first.")
            return

        reply = self.reply_input.toPlainText().strip()

        if not reply:
            show_error(self, "Error", "Reply cannot be empty.")
            return

        self.db.send_message(
            sender_type="librarian",
            sender_id=1,
            receiver_type="user",
            receiver_id=self.selected_request_user_id,
            subject="Book Request Reply",
            message=reply
        )

        self.db.delete_book_request(self.selected_request_id)

        show_info(self, "Success", "Reply sent and request removed.")
        self.load_requests()

    def delete_selected_request(self):
        if not self.selected_request_id:
            show_error(self, "Error", "Select a book request first.")
            return

        confirm = show_confirm(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this book request?"
        )

        if confirm != QMessageBox.Yes:
            return

        self.db.delete_book_request(self.selected_request_id)
        show_info(self, "Success", "Book request deleted.")
        self.load_requests()