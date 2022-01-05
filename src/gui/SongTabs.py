from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QSizePolicy, QTabWidget, QWidget,
                               QHBoxLayout)

from src.gui.SongDisplay import QScrollableSongDisplay
from src.gui.SongList import ScrollAndSearchSongList

from pynput import keyboard

class QSongTabs(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('HK Songbook')
        icon = QIcon("guitar.ico")
        self.setWindowIcon(icon)
        layout = QHBoxLayout()

        songList = ScrollAndSearchSongList()
        songList.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        songList.setMinimumWidth(350)
        songList.scrollableSongList.songList.openSongDisplay = self.openSongDisplay
        layout.addWidget(songList)

        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.tabWidget)

        self.setLayout(layout)

        self.tabsLoaded = False
        self.altPressed = False

        self.tabWidget.tabInserted = self.openSong
        self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)

        self.listener = keyboard.Listener(
            on_press=self.onPress,
            on_release=self.onRelease)
        self.listener.start()

        self.repaint()

        self.showMaximized()

    def closeEvent(self, event):
        self.listener.stop()
        event.accept()

    def openSong(self, index):
        if not self.altPressed:
            self.tabWidget.setCurrentIndex(index)

    def openSongDisplay(self, link):
        cat, _, song = link.partition('#')
        self.tabWidget.addTab(QScrollableSongDisplay(cat, song), song)

    def onPress(self, key):
        if key in [keyboard.Key.alt, keyboard.Key.alt_l]:
            self.altPressed = True

    def onRelease(self, key):
        if key in [keyboard.Key.alt, keyboard.Key.alt_l]:
            self.altPressed = False
