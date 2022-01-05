from PySide6.QtWidgets import QApplication
from src.gui.SongTabs import QSongTabs

import sys

app = QApplication(sys.argv)
window = QSongTabs()
app.exec()
