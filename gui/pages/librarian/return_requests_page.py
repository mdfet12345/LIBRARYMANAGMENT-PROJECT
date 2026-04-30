from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHBoxLayout,
    QComboBox
)
from PyQt5.QtCore import Qt

from database.database_manager import DatabaseManager
from functions.ui_messages import show_info, show_error


class ReturnRequestsPage(QWidget):
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

            QComboBox {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 6px;
                padding: 8px;
                min-width: 160px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        title = QLabel("Return Requests")
        title.setObjectName("title")

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Request ID",
            "Customer",
            "Book",
            "Borrow Date",
            "Last Return Date",
            "Borrow ID"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0)
        self.table.hideColumn(5)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.condition_box = QComboBox()
        self.condition_box.addItems(["Excellent", "Good", "Bad", "Damaged"])

        self.approve_btn = QPushButton("Issue Return")
        self.approve_btn.clicked.connect(self.approve_selected_return)

        bottom_layout.addWidget(self.condition_box)
        bottom_layout.addWidget(self.approve_btn)

        layout.addWidget(title)
        layout.addWidget(self.table, 1)
        layout.addLayout(bottom_layout)

    def load_requests(self):
        requests = self.db.get_pending_return_requests()

        self.table.setRowCount(0)

        for row_index, request in enumerate(requests):
            self.table.insertRow(row_index)

            for col_index, value in enumerate(request):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

        self.table.resizeColumnsToContents()

    def approve_selected_return(self):
        selected_row = self.table.currentRow()

        if selected_row < 0:
            show_error(self, "Error", "Please select a return request first.")
            return

        request_id = int(self.table.item(selected_row, 0).text())
        condition = self.condition_box.currentText()

        success, result = self.db.approve_return(request_id, condition)

        if success:
            show_info(
                self,
                "Return Complete",
                f"Book return is complete.\nMember is fined: ${result:.2f}"
            )
            self.load_requests()
        else:
            show_error(self, "Error", result)