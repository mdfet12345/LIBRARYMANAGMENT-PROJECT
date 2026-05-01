from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PyQt5.QtCore import Qt
from gui.pages.librarian.return_requests_page import ReturnRequestsPage
from gui.pages.librarian.manage_members_page import ManageMembersPage
from gui.pages.librarian.add_book_page import AddBookPage
from gui.pages.librarian.manage_books_page import ManageBooksPage
from gui.pages.librarian.messages_page import LibrarianMessagesPage
from gui.pages.librarian.borrowed_books_page import BorrowedBooksPage

class LibrarianDashboard(QWidget):
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

            QLabel#title {
                color: white;
                font-size: 20px;
                font-weight: 800;
                background-color: transparent;
                border: none;
            }

            QPushButton#navButton {
                background-color: transparent;
                color: #f2f2f2;
                border: none;
                border-radius: 8px;
                padding: 12px;
                text-align: left;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#navButton:hover {
                background-color: #3a3a3a;
            }

            QPushButton#logoutButton {
                background-color: white;
                color: #2b2b2b;
                border-radius: 8px;
                padding: 12px;
                font-weight: 700;
            }
            QLabel {
                background-color: transparent;
            }

            QPushButton#logoutButton:hover {
                background-color: #eeeeee;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # -------------------------
        # SIDEBAR
        # -------------------------
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 24, 18, 18)
        sidebar_layout.setSpacing(10)

        title = QLabel("Librarian")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.btn_dashboard = QPushButton("📊  Dashboard")
        self.btn_books = QPushButton("📚  Manage Books")
        self.btn_add_book = QPushButton("➕  Add Book")
        self.btn_borrowed = QPushButton("📖  Borrowed Books")
        self.btn_returns = QPushButton("🔄  Return Requests")
        self.btn_members = QPushButton("👥  Members")
        self.btn_messages = QPushButton("📩  Requests")
        self.btn_logout = QPushButton("Logout")

        for btn in [
            self.btn_dashboard,
            self.btn_books,
            self.btn_add_book,
            self.btn_borrowed,
            self.btn_returns,
            self.btn_members,
            self.btn_messages
        ]:
            btn.setObjectName("navButton")
            btn.setCursor(Qt.PointingHandCursor)

        self.btn_logout.setObjectName("logoutButton")

        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_books)
        sidebar_layout.addWidget(self.btn_add_book)
        sidebar_layout.addWidget(self.btn_borrowed)
        sidebar_layout.addWidget(self.btn_returns)
        sidebar_layout.addWidget(self.btn_members)
        sidebar_layout.addWidget(self.btn_messages)

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_logout)

        # -------------------------
        # CONTENT AREA
        # -------------------------
        self.stack = QStackedWidget()

        self.page_dashboard = self.create_dashboard_page()
        self.page_books = ManageBooksPage(self.main_window)
        self.page_add_book = AddBookPage(self.main_window)
        self.page_borrowed = BorrowedBooksPage(self.main_window)
        self.page_returns = ReturnRequestsPage(self.main_window)
        self.page_members = ManageMembersPage(self.main_window)
        self.page_messages = LibrarianMessagesPage(self.main_window)

        self.stack.addWidget(self.page_dashboard)
        self.stack.addWidget(self.page_books)
        self.stack.addWidget(self.page_add_book)
        self.stack.addWidget(self.page_borrowed)
        self.stack.addWidget(self.page_returns)
        self.stack.addWidget(self.page_members)
        self.stack.addWidget(self.page_messages)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack, 1)

        # -------------------------
        # NAVIGATION
        # -------------------------
        self.btn_dashboard.clicked.connect(self.open_dashboard)
        self.btn_books.clicked.connect(self.open_books)
        self.btn_add_book.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_add_book))
        self.btn_borrowed.clicked.connect(self.open_borrowed_books)
        self.btn_returns.clicked.connect(self.open_returns)
        self.btn_members.clicked.connect(self.open_members)
        self.btn_messages.clicked.connect(self.open_messages)
        self.btn_logout.clicked.connect(self.logout)

    def create_placeholder(self, text):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: 700;
                color: #444;
            }
        """)

        layout.addWidget(label)
        return page

    def logout(self):
        self.main_window.go_to_login_selection()
    def create_dashboard_page(self):
        from database.database_manager import DatabaseManager
        from PyQt5.QtWidgets import QGridLayout

        db = DatabaseManager()
        stats = db.get_librarian_dashboard_stats()

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Dashboard")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: 800;
                color: #1a1a1a;
                background: transparent;
            }
        """)

        grid = QGridLayout()
        grid.setSpacing(20)

        def create_card(label, value, color):
            card = QFrame()
            card.setMinimumHeight(120)

            card.setStyleSheet(f"""
                QFrame {{
                    background-color: white;
                    border-radius: 12px;
                    border-left: 6px solid {color};
                }}
            """)

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(18, 14, 18, 14)
            card_layout.setSpacing(8)

            value_label = QLabel(str(value))
            value_label.setStyleSheet("""
                QLabel {
                    font-size: 28px;
                    font-weight: 800;
                    color: #111111;
                    background: transparent;
                }
            """)

            label_text = QLabel(label)
            label_text.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #666666;
                    background: transparent;
                }
            """)

            card_layout.addWidget(value_label)
            card_layout.addWidget(label_text)
            card_layout.addStretch()

            return card

        cards = [
            ("Total Books", stats["total_books"], "#4fa3ff"),
            ("Borrowed Books", stats["borrowed_books"], "#f39c12"),
            ("Members", stats["total_members"], "#2ecc71"),
            ("Overdue", stats["overdue_books"], "#e74c3c"),
            ("Pending Returns", stats["pending_returns"], "#9b59b6"),
            ("Unverified Members", stats["unverified_members"], "#e67e22"),
            ("Book Requests", stats["book_requests"], "#16a085"),
        ]

        for i, (label, value, color) in enumerate(cards):
            row = i // 3
            col = i % 3
            grid.addWidget(create_card(label, value, color), row, col)

        for i in range(3):
            grid.setColumnStretch(i, 1)

        layout.addWidget(title)
        layout.addLayout(grid)
        layout.addStretch()
        return page
    
    
    def open_dashboard(self):
        index = self.stack.indexOf(self.page_dashboard)

        if index != -1:
            old_page = self.page_dashboard
            self.stack.removeWidget(old_page)
            old_page.deleteLater()

        self.page_dashboard = self.create_dashboard_page()
        self.stack.insertWidget(0, self.page_dashboard)
        self.stack.setCurrentWidget(self.page_dashboard)
    
    
    def open_returns(self):
        self.page_returns.load_requests()
        self.stack.setCurrentWidget(self.page_returns)
    
    def open_members(self):
        self.page_members.load_members()
        self.stack.setCurrentWidget(self.page_members)
        
    def open_books(self):
        self.page_books.load_books()
        self.stack.setCurrentWidget(self.page_books)
    
    def open_messages(self):
        self.page_messages.load_messages()
        self.page_messages.load_requests()
        self.stack.setCurrentWidget(self.page_messages)
    def open_borrowed_books(self):
        self.page_borrowed.load_borrowed_books()
        self.stack.setCurrentWidget(self.page_borrowed)
    