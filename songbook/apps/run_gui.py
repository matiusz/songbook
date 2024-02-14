from PySide6.QtWidgets import QApplication

from ..src.gui.MainMenu import MainMenu

import sys

def main():
    app = QApplication(sys.argv)
    window = MainMenu()
    app.exec()

if __name__ == "__main__":
    main()