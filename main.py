import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from gui.main_window import MainWindow
import os
app = QApplication(sys.argv)
base_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(base_dir, "fonts", "FRADM.TTF")

font_id = QFontDatabase.addApplicationFont(font_path)



# -------------------------
# LOAD CUSTOM FONT (ONLY LOAD, DON'T APPLY)
# -------------------------
#font_id = QFontDatabase.addApplicationFont("fonts/FRADM.TTF")

if font_id != -1:
    family = QFontDatabase.applicationFontFamilies(font_id)[0]
    print(f"Loaded font: {family}")
else:
    print("Font failed to load")

# -------------------------
# SET CLEAN GLOBAL FONT
# -------------------------
app.setFont(QFont("Segoe UI", 10))

# -------------------------
# START APP
# -------------------------
window = MainWindow()
window.show()

sys.exit(app.exec_())