from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit
)
from PyQt5.QtCore import Qt

from database.database_manager import DatabaseManager
from functions.ui_messages import show_info, show_error, show_confirm
from PyQt5.QtWidgets import QMessageBox


class ManageMembersPage(QWidget):
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
            
            QLineEdit {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
                color: #111111;
            }

            QLineEdit:focus {
                border: 1px solid #2b2b2b;
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
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        title = QLabel("Manage Members")
        title.setObjectName("title")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search members by name, username, national ID, email, verification, or fines...")

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Username", "National ID", "Age", "Email", "Verified", "Fines"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.verify_btn = QPushButton("Verify Member")
        self.unverify_btn = QPushButton("Un-verify Member")
        self.clear_fines_btn = QPushButton("Clear Fines")
        self.delete_btn = QPushButton("Delete Member")

        buttons_layout.addWidget(self.verify_btn)
        buttons_layout.addWidget(self.unverify_btn)
        buttons_layout.addWidget(self.clear_fines_btn)
        buttons_layout.addWidget(self.delete_btn)

        layout.addWidget(title)
        layout.addWidget(self.search_input)
        layout.addWidget(self.table, 1)
        layout.addLayout(buttons_layout)

        self.verify_btn.clicked.connect(self.verify_selected_member)
        self.unverify_btn.clicked.connect(self.unverify_selected_member)
        self.clear_fines_btn.clicked.connect(self.clear_selected_fines)
        self.delete_btn.clicked.connect(self.delete_selected_member)
        self.search_input.textChanged.connect(self.filter_members)

    def load_members(self):
        users = self.db.get_all_users()
        self.table.setRowCount(0)

        for row_index, user in enumerate(users):
            user_id = user[0]
            name = user[1]
            username = user[2]
            national_id = user[3]
            age = user[4]
            email = user[5]
            is_verified = "Yes" if user[7] == 1 else "No"
            fines = f"${user[8]:.2f}"

            row_data = [
                user_id, name, username, national_id, age, email, is_verified, fines
            ]

            self.table.insertRow(row_index)

            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

        self.table.resizeColumnsToContents()
        self.filter_members()
    
    
    # search function    
    def filter_members(self):
        search_text = self.search_input.text().strip().lower()

        for row in range(self.table.rowCount()):
            row_matches = False

            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)

                if item and search_text in item.text().lower():
                    row_matches = True
                    break

            self.table.setRowHidden(row, not row_matches)

    def get_selected_user_id(self):
        selected_row = self.table.currentRow()

        if selected_row < 0:
            show_error(self, "Error", "Please select a member first")
            return None

        return int(self.table.item(selected_row, 0).text())

    def verify_selected_member(self):
        user_id = self.get_selected_user_id()
        if user_id is None:
            return

        selected_row = self.table.currentRow()
        verified_status = self.table.item(selected_row, 6).text()

        if verified_status == "Yes":
            show_info(self, "Already Verified", "This member is already verified")
            return

        self.db.verify_user(user_id)
        show_info(self, "Success", "Member verified successfully")
        self.load_members()
        

    def unverify_selected_member(self):
        user_id = self.get_selected_user_id()
        if user_id is None:
            return

        selected_row = self.table.currentRow()
        verified_status = self.table.item(selected_row, 6).text()

        if verified_status == "No":
            show_info(self, "Already Unverified", "This member is already unverified")
            return

        self.db.unverify_user(user_id)
        show_info(self, "Success", "Member unverified successfully")
        self.load_members()
        
        
    def clear_selected_fines(self):
        user_id = self.get_selected_user_id()
        if user_id is None:
            return

        selected_row = self.table.currentRow()
        fines_text = self.table.item(selected_row, 7).text()
        fines_amount = float(fines_text.replace("$", ""))

        if fines_amount == 0:
            show_info(self, "No Fines", "This member has no fines to clear")
            return

        self.db.clear_fines(user_id)
        show_info(self, "Success", "Member fines cleared")
        self.load_members()

    def delete_selected_member(self):
        user_id = self.get_selected_user_id()

        if user_id is None:
            return

        confirm = show_confirm(
            self,
            "Confirm Delete",
            "Are you sure you want to permanently delete this member?"
        )

        if confirm != QMessageBox.Yes:
            return

        success, message = self.db.delete_user(user_id)

        if success:
            show_info(self, "Success", message)
            self.load_members()
        else:
            show_error(self, "Error", message)