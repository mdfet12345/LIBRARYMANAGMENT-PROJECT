from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt

from functions.auth_functions import check_customer_login
from functions.ui_messages import show_error, show_info


class CustomerLoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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
                min-height: 40px;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(420)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 35, 35, 35)
        card_layout.setSpacing(15)

        title = QLabel("Customer Login")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        back_btn = QPushButton("Back")

        card_layout.addWidget(title)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.password)
        card_layout.addSpacing(10)
        card_layout.addWidget(login_btn)
        card_layout.addWidget(back_btn)

        main_layout.addStretch()
        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        login_btn.clicked.connect(self.login)
        back_btn.clicked.connect(self.go_back)

    def login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        success, result = check_customer_login(username, password)

        if not success:
            show_error(self, "Login Failed", result)
            return

        self.main_window.current_user = result
        self.main_window.page_customer_dashboard.update_customer_info()
        self.main_window.go_to_customer_dashboard()

    def go_back(self):
        self.main_window.go_to_login_selection()