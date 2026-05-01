from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QLineEdit, QHBoxLayout, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView

from database.database_manager import DatabaseManager


class BorrowedBooksPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = DatabaseManager()
        self.records = []
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

            QLineEdit {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                min-height: 34px;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #eeeeee;
                border-radius: 10px;
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
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        title = QLabel("Borrowed Books")
        title.setObjectName("title")

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by customer, username, or book title...")
        self.search_input.textChanged.connect(self.apply_filter)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["ALL", "Overdue", "On Time"])
        self.status_filter.currentTextChanged.connect(self.apply_filter)

        filter_layout.addWidget(self.search_input, 2)
        filter_layout.addWidget(self.status_filter, 1)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Borrow ID", "Customer", "Username", "Book",
            "Borrow Date", "Return Date", "Status"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setStretchLastSection(True)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(title)
        layout.addLayout(filter_layout)
        layout.addWidget(self.table, 1)

    def load_borrowed_books(self):
        self.records = self.db.get_all_borrowed_books()
        self.display_records(self.records)

    def display_records(self, records):
        self.table.setRowCount(0)

        for row, record in enumerate(records):
            self.table.insertRow(row)

            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

    def apply_filter(self):
        keyword = self.search_input.text().strip().lower()
        selected_status = self.status_filter.currentText()

        filtered = []

        for record in self.records:
            customer = str(record[1]).lower()
            username = str(record[2]).lower()
            book = str(record[3]).lower()
            status = str(record[6])

            matches_keyword = (
                not keyword
                or keyword in customer
                or keyword in username
                or keyword in book
            )

            matches_status = (
                selected_status == "ALL"
                or selected_status == status
            )

            if matches_keyword and matches_status:
                filtered.append(record)

        self.display_records(filtered)