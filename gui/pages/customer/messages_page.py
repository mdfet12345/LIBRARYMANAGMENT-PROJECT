from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QTabWidget,
    QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt

from database.database_manager import DatabaseManager
from functions.ui_messages import show_info, show_error


class CustomerMessagesPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = DatabaseManager()

        self.replies = []
        self.selected_reply_id = None

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
                font-size: 14px;
                color: #555555;
            }

            QLineEdit, QTextEdit {
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

            QTabWidget::pane {
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        title = QLabel("Requests")
        title.setObjectName("title")

        self.tabs = QTabWidget()
        self.request_tab = self.create_request_tab()
        self.replies_tab = self.create_replies_tab()

        self.tabs.addTab(self.request_tab, "Request Book")
        self.tabs.addTab(self.replies_tab, "Replies")

        layout.addWidget(title)
        layout.addWidget(self.tabs)

    def load_messages(self):
        self.load_replies()

    def create_request_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(12)

        self.book_title_input = QLineEdit()
        self.book_title_input.setPlaceholderText("Book Title")

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author (optional)")

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes (optional)")
        self.notes_input.setMinimumHeight(180)

        request_btn = QPushButton("Submit Request")
        request_btn.clicked.connect(self.request_book)

        layout.addWidget(QLabel("Book Title"))
        layout.addWidget(self.book_title_input)
        layout.addWidget(QLabel("Author"))
        layout.addWidget(self.author_input)
        layout.addWidget(QLabel("Notes"))
        layout.addWidget(self.notes_input)
        layout.addWidget(request_btn)
        layout.addStretch()

        return tab

    def request_book(self):
        user = self.main_window.current_user

        if not user:
            show_error(self, "Error", "Please login first.")
            return

        title = self.book_title_input.text().strip()
        author = self.author_input.text().strip()
        notes = self.notes_input.toPlainText().strip()

        if not title:
            show_error(self, "Error", "Book title is required.")
            return

        try:
            self.db.create_book_request(user["id"], title, author, notes)

            show_info(self, "Success", "Book request submitted.")

            self.book_title_input.clear()
            self.author_input.clear()
            self.notes_input.clear()

        except Exception as e:
            show_error(self, "Error", f"Could not submit book request:\n{str(e)}")

    def create_replies_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(12)

        self.replies_table = QTableWidget()
        self.replies_table.setColumnCount(3)
        self.replies_table.setHorizontalHeaderLabels(["Reply ID", "Subject", "Date"])
        self.replies_table.hideColumn(0)
        self.replies_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.replies_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.replies_table.cellClicked.connect(self.show_reply_details)

        self.reply_view = QTextEdit()
        self.reply_view.setReadOnly(True)
        self.reply_view.setPlaceholderText("Select a reply to read...")

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.delete_reply_btn = QPushButton("Delete Reply")
        self.delete_reply_btn.setObjectName("deleteBtn")
        self.delete_reply_btn.clicked.connect(self.delete_selected_reply)

        button_layout.addWidget(self.delete_reply_btn)

        layout.addWidget(self.replies_table, 2)
        layout.addWidget(self.reply_view, 1)
        layout.addLayout(button_layout)

        return tab

    def load_replies(self):
        user = self.main_window.current_user

        if not user:
            return

        self.replies = self.db.get_request_replies_for_user(user["id"])
        self.selected_reply_id = None
        self.reply_view.clear()

        self.replies_table.setRowCount(0)

        for row, reply in enumerate(self.replies):
            self.replies_table.insertRow(row)

            reply_id = reply[0]
            subject = reply[1] or "Request Reply"
            date = reply[3]

            row_data = [reply_id, subject, date]

            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.replies_table.setItem(row, col, item)

        self.replies_table.resizeColumnsToContents()

    def show_reply_details(self, row, col):
        reply = self.replies[row]

        self.selected_reply_id = reply[0]

        subject = reply[1] or "Request Reply"
        message = reply[2]
        date = reply[3]

        self.reply_view.setText(
            f"Subject: {subject}\n"
            f"From: Librarian\n"
            f"Date: {date}\n\n"
            f"{message}"
        )

    def delete_selected_reply(self):
        if not self.selected_reply_id:
            show_error(self, "Error", "Select a reply first.")
            return

        self.db.delete_message(self.selected_reply_id)
        show_info(self, "Success", "Reply deleted.")
        self.load_replies()