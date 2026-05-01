from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont


def _base_message(parent, title, message, icon):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(icon)

    msg.setStyleSheet("""
        QMessageBox {
            background-color: #ffffff;
        }

        QLabel {
            color: #1a1a1a;
            font-size: 14px;
        }

        QPushButton {
            background-color: #2b2b2b;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            min-width: 90px;
            min-height: 34px;
            font-size: 13px;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #3a3a3a;
        }

        QPushButton:pressed {
            background-color: #111111;
        }
    """)

    msg.setFont(QFont("Segoe UI", 10))
    msg.exec_()



# info

def show_info(parent, title, message):
    _base_message(parent, title, message, QMessageBox.Information)


# -------------------------
# WARNING
# -------------------------
def show_warning(parent, title, message):
    _base_message(parent, title, message, QMessageBox.Warning)


# -------------------------
# ERROR
# -------------------------
def show_error(parent, title, message):
    _base_message(parent, title, message, QMessageBox.Critical)


# -------------------------
# CONFIRM (VERY IMPORTANT)
# -------------------------
def show_confirm(parent, title, message):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    msg.setStyleSheet("""
        QMessageBox {
            background-color: #ffffff;
        }

        QMessageBox QLabel {
            color: #1a1a1a;
            font-size: 14px;
            background-color: transparent;
        }

        QMessageBox QPushButton {
            background-color: #2b2b2b;
            color: #ffffff;
            border: 1px solid #2b2b2b;
            border-radius: 8px;
            padding: 8px 18px;
            min-width: 80px;
            min-height: 34px;
            font-size: 13px;
            font-weight: bold;
        }

        QMessageBox QPushButton:hover {
            background-color: #3a3a3a;
            border: 1px solid #3a3a3a;
        }

        QMessageBox QPushButton:disabled {
            background-color: #2b2b2b;
            color: #ffffff;
        }
    """)

    for button in msg.buttons():
        button.setAutoDefault(False)
        button.setDefault(False)
    yes_button = msg.button(QMessageBox.Yes)
    no_button = msg.button(QMessageBox.No)

    for button in [yes_button, no_button]:
        if button:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2b2b2b;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 18px;
                    min-width: 80px;
                    min-height: 34px;
                    font-size: 13px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #3a3a3a;
                }
            """)

    return msg.exec_()