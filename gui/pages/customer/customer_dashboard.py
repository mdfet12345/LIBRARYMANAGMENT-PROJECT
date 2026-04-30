from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PyQt5.QtCore import Qt

from gui.pages.customer.browse_books import BrowseBooksPage
from gui.pages.customer.cart_page import CartPage
from gui.pages.customer.personal_books_page import PersonalBooksPage
from gui.pages.customer.messages_page import CustomerMessagesPage


class CustomerDashboard(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
            }

            QFrame#sidebar {
                background-color: #2b2b2b;
            }

            QLabel {
                background: transparent;
            }

            QLabel#userLabel {
                color: white;
                font-size: 18px;
                font-weight: 700;
            }

            QLabel#fineLabel {
                color: #d7d7d7;
                font-size: 13px;
            }

            QPushButton#navButton {
                background-color: transparent;
                color: #f2f2f2;
                border: none;
                border-radius: 8px;
                padding: 12px 14px;
                text-align: left;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#navButton:hover {
                background-color: #3a3a3a;
            }

            QPushButton#logoutButton {
                background-color: #ffffff;
                color: #2b2b2b;
                border: none;
                border-radius: 8px;
                padding: 12px 14px;
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton#logoutButton:hover {
                background-color: #eeeeee;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(18, 24, 18, 18)
        sidebar_layout.setSpacing(10)

        self.user_label = QLabel("Customer")
        self.user_label.setObjectName("userLabel")
        self.user_label.setAlignment(Qt.AlignCenter)

        self.fine_label = QLabel("Fines: $0.00")
        self.fine_label.setObjectName("fineLabel")
        self.fine_label.setAlignment(Qt.AlignCenter)

        self.btn_browse = QPushButton("📚  Browse Books")
        self.btn_cart = QPushButton("🛒  My Cart")
        self.btn_personal = QPushButton("📖  Personal Books")
        self.btn_requests = QPushButton("📩  Request a Book")
        self.btn_logout = QPushButton("Logout")

        for btn in [
            self.btn_browse,
            self.btn_cart,
            self.btn_personal,
            self.btn_requests
        ]:
            btn.setObjectName("navButton")
            btn.setCursor(Qt.PointingHandCursor)

        self.btn_logout.setObjectName("logoutButton")
        self.btn_logout.setCursor(Qt.PointingHandCursor)

        sidebar_layout.addWidget(self.user_label)
        sidebar_layout.addWidget(self.fine_label)
        sidebar_layout.addSpacing(25)

        sidebar_layout.addWidget(self.btn_browse)
        sidebar_layout.addWidget(self.btn_cart)
        sidebar_layout.addWidget(self.btn_personal)
        sidebar_layout.addWidget(self.btn_requests)

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_logout)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("""
            QStackedWidget {
                background-color: #fafafa;
            }
        """)

        self.page_browse = BrowseBooksPage(self.main_window)
        self.page_cart = CartPage(self.main_window)
        self.page_personal = PersonalBooksPage(self.main_window)
        self.page_messages = CustomerMessagesPage(self.main_window)

        self.stack.addWidget(self.page_browse)
        self.stack.addWidget(self.page_cart)
        self.stack.addWidget(self.page_personal)
        self.stack.addWidget(self.page_messages)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack, 1)

        self.btn_browse.clicked.connect(self.open_browse)
        self.btn_cart.clicked.connect(self.open_cart)
        self.btn_personal.clicked.connect(self.open_personal_books)
        self.btn_requests.clicked.connect(self.open_requests)
        self.btn_logout.clicked.connect(self.logout)

        self.stack.setCurrentWidget(self.page_browse)

    def update_customer_info(self):
        user = self.main_window.current_user

        if not user:
            return

        self.user_label.setText(user["name"])

        fine = user.get("fine_amount", 0)
        self.fine_label.setText(f"Fines: ${fine:.2f}")

    def open_browse(self):
        self.page_browse.load_books()
        self.stack.setCurrentWidget(self.page_browse)

    def open_cart(self):
        self.page_cart.load_cart()
        self.stack.setCurrentWidget(self.page_cart)

    def open_personal_books(self):
        self.page_personal.load_books()
        self.stack.setCurrentWidget(self.page_personal)

    def open_requests(self):
        self.page_messages.load_messages()
        self.stack.setCurrentWidget(self.page_messages)

    def logout(self):
        self.main_window.current_user = None
        self.main_window.go_to_login_selection()