from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt

from functions.auth_functions import check_librarian_login
from functions.ui_messages import show_error, show_info


class LibrarianLoginPage(QWidget):
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

        # CARD
        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(420)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 35, 35, 35)
        card_layout.setSpacing(15)

        # TITLE
        title = QLabel("Librarian Login")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # INPUTS
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        # BUTTONS
        login_btn = QPushButton("Login")
        back_btn = QPushButton("Back")

        # ADD
        card_layout.addWidget(title)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.password)
        card_layout.addSpacing(10)
        card_layout.addWidget(login_btn)
        card_layout.addWidget(back_btn)

        # CENTER
        main_layout.addStretch()
        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        # ACTIONS
        login_btn.clicked.connect(self.login)
        back_btn.clicked.connect(self.go_back)

    def login(self):
        username = self.username.text()
        password = self.password.text()

        if check_librarian_login(username, password):
            self.main_window.go_to_librarian_dashboard()
        else:
            show_error(self, "Login Failed", "Invalid username or password")

    def go_back(self):
        self.main_window.go_to_login_selection()
        
    def clear_fields(self):
        self.username.clear()
        self.password.clear()