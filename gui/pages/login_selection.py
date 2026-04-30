from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt


class LoginSelectionPage(QWidget):
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

            /* 🔥 FORCE ALL TEXT ELEMENTS CLEAN */
            QLabel {
                background-color: transparent;
                border: none;
                padding: 0px;
            }

            QLabel#title {
                font-family: "Franklin Gothic Demi";
                font-size: 26px;
                font-weight: bold;
                color: #111111;
            }

            QLabel#subtitle {
                font-size: 15px;
                color: #666666;
            }

            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
                min-height: 42px;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }

            QPushButton:pressed {
                background-color: #151515;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        card = QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(430)
        card.setMaximumWidth(500)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(35, 35, 35, 35)
        card_layout.setSpacing(14)
        card.setLayout(card_layout)

        title = QLabel("Library Management System")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setMinimumHeight(65)

        subtitle = QLabel("Select your login type")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setMinimumHeight(28)

        librarian_btn = QPushButton("Login as Librarian")
        customer_btn = QPushButton("Login as Customer")
        register_btn = QPushButton("Register Customer")

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(8)
        card_layout.addWidget(librarian_btn)
        card_layout.addWidget(customer_btn)
        card_layout.addWidget(register_btn)

        main_layout.addStretch()
        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        librarian_btn.clicked.connect(self.go_librarian_login)
        customer_btn.clicked.connect(self.go_customer_login)
        register_btn.clicked.connect(self.register_customer)

    def go_librarian_login(self):
        self.main_window.go_to_librarian()

    def go_customer_login(self):
        self.main_window.go_to_customer()

    def register_customer(self):
        self.main_window.stack.setCurrentWidget(self.main_window.page_register)