from PySide6.QtWidgets import QApplication

from ..src.gui.MainMenu import MainMenu

import sys

app = QApplication(sys.argv)
window = MainMenu()
app.exec()
