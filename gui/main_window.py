from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QSizePolicy
)
from PyQt5.QtCore import QTimer

from gui.pages.login_selection import LoginSelectionPage
from gui.pages.librarian_login import LibrarianLoginPage
from gui.pages.customer_login import CustomerLoginPage
from gui.pages.register_customer import RegisterCustomerPage
from gui.pages.customer.customer_dashboard import CustomerDashboard
from gui.pages.librarian.librarian_dashboard import LibrarianDashboard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Library Management System")
        self.resize(1300, 800)
        self.setMinimumSize(1200, 700)
        

        # central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)   
        self.layout.setSpacing(0)                    
        self.central_widget.setLayout(self.layout)

        # stacked widget
        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.stack)

        # pages

        self.page_login_selection = LoginSelectionPage(self)
        self.page_librarian = LibrarianLoginPage(self)
        self.page_customer = CustomerLoginPage(self)
        self.page_register = RegisterCustomerPage(self)
        self.page_customer_dashboard = CustomerDashboard(self)
        self.page_librarian_dashboard = LibrarianDashboard(self)


        self.stack.addWidget(self.page_login_selection)
        self.stack.addWidget(self.page_librarian)
        self.stack.addWidget(self.page_customer)
        self.stack.addWidget(self.page_register)
        self.stack.addWidget(self.page_customer_dashboard)
        self.stack.addWidget(self.page_librarian_dashboard)

        self.stack.setCurrentWidget(self.page_login_selection)

        # user session
        self.current_user = None

        # apply tyle
        self.apply_styles()

    # navigation
    
    def go_to_login_selection(self):
        self.stack.setCurrentWidget(self.page_login_selection)

    def go_to_librarian_login(self):
        self.page_librarian.clear_fields()
        self.stack.setCurrentWidget(self.page_librarian)

    def go_to_customer_login(self):
        self.page_customer.clear_fields()
        self.stack.setCurrentWidget(self.page_customer)

    def go_to_register(self):
        self.page_register.clear_fields()
        self.stack.setCurrentWidget(self.page_register)

    def go_to_customer_dashboard(self):
        self.page_customer_dashboard.update_customer_info()
        self.page_customer_dashboard.page_browse.load_books()
        self.page_customer_dashboard.stack.setCurrentWidget(
            self.page_customer_dashboard.page_browse
        )
        self.stack.setCurrentWidget(self.page_customer_dashboard)

    def go_to_librarian_dashboard(self):
        self.page_librarian_dashboard.open_dashboard()
        self.stack.setCurrentWidget(self.page_librarian_dashboard)

    # style 

    def apply_styles(self):
        self.setStyleSheet("""
                QMainWindow {
                    background-color: #fafafa;
                    font-size: 14px;
                }

                QLabel {
                    color: #1a1a1a;
                    background: transparent;
                }

                QPushButton {
                    background-color: #4fa3ff;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 8px;
                    min-height: 40px;
                    font-weight: 600;
                }

                QPushButton:hover {
                    background-color: #2f8de4;
                }

                QPushButton:pressed {
                    background-color: #1f6fbf;
                }

                QLineEdit, QComboBox {
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 6px;
                    background-color: white;
                }

                QFrame {
                    background: transparent;
                }
            """)