from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame,
    QCheckBox
)
from PyQt5.QtCore import Qt
import re

from database.database_manager import DatabaseManager
from functions.ui_messages import show_error, show_info


class RegisterCustomerPage(QWidget):
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

            QFrame#card {
                background-color: #ffffff;
                border-radius: 16px;
            }

            QLabel {
                background: transparent;
                border: none;
            }

            QLabel#title {
                font-family: "Franklin Gothic Demi";
                font-size: 24px;
                font-weight: bold;
                color: #111111;
            }

            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #4fa3ff;
            }

            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                min-height: 38px;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(440)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 35, 35, 35)
        card_layout.setSpacing(12)

        title = QLabel("Customer Registration")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Full Name")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        
        self.terms_checkbox = QCheckBox("I accept the Terms of Use and Privacy Policy")
        self.terms_checkbox.setStyleSheet("""
            QCheckBox {
                background: transparent;
                color: #2b2b2b;
                font-size: 13px;
            }
        """)
        

        register_btn = QPushButton("Create Account")
        back_btn = QPushButton("Back")

        card_layout.addWidget(title)
        card_layout.addWidget(self.name)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.age)
        card_layout.addWidget(self.email)
        card_layout.addWidget(self.password)
        card_layout.addSpacing(8)
        card_layout.addWidget(self.terms_checkbox)
        card_layout.addWidget(register_btn)
        card_layout.addWidget(back_btn)

        main_layout.addStretch()
        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        register_btn.clicked.connect(self.register)
        back_btn.clicked.connect(self.go_back)

    def register(self):
        name = self.name.text().strip()
        username = self.username.text().strip()
        age = self.age.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        
        if not self.terms_checkbox.isChecked():
            show_error(self, "Error", "You must accept the Terms of Use and Privacy Policy to register.")
            return

        if not all([name, username, age, email, password]):
            show_error(self, "Error", "All fields are required")
            return

        if not age.isdigit():
            show_error(self, "Error", "Age must be a number")
            return

        age = int(age)

        if age < 18:
            show_error(self, "Error", "You must be at least 18 years old")
            return

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(email_pattern, email):
            show_error(self, "Error", "Invalid email format")
            return

        if len(password) < 8:
            show_error(self, "Error", "Password must be at least 8 characters")
            return

        if not re.search(r"[A-Z]", password):
            show_error(self, "Error", "Password must contain an uppercase letter")
            return

        if not re.search(r"[a-z]", password):
            show_error(self, "Error", "Password must contain a lowercase letter")
            return

        if not re.search(r"[0-9]", password):
            show_error(self, "Error", "Password must contain a number")
            return

        success = self.db.register_user(
            name, username, age, email, password
        )

        if success:
            show_info(self, "Success", "Account created! Wait for librarian verification.")
            self.clear_fields()
            self.main_window.go_to_login_selection()
        else:
            show_error(self, "Error", "Username or email already exists")

    def clear_fields(self):
        self.name.clear()
        self.username.clear()
        self.age.clear()
        self.email.clear()
        self.password.clear()
        self.terms_checkbox.setChecked(False)

    def go_back(self):
        self.main_window.go_to_login_selection()