from PySide6.QtWidgets import (QSizePolicy, QTabWidget, QWidget, 
                                QHBoxLayout)

from src.gui.SongDisplay import QScrollableSongDisplay
from src.gui.SongList import ScrollAndSearchSongList



class QSongTabs(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(0, 0, 400, 1000)
        
        layout = QHBoxLayout()
        songList = ScrollAndSearchSongList()
        songList.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        songList.setMinimumWidth(300)
        
        songList.scrollableSongList.songList.openSongDisplay = self.openSongDisplay
        layout.addWidget(songList)
        
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout.addWidget(self.tabWidget)

        self.setLayout(layout)
        
        self.tabsLoaded = False

        self.tabWidget.tabInserted = self.tabWidget.setCurrentIndex
        self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)


        self.repaint()
        
        self.show()
        
    def openSongDisplay(self, link):
        cat, _, song = link.partition('#')
        self.tabWidget.addTab(QScrollableSongDisplay(cat, song), song)
        if not self.tabsLoaded:
            self.setGeometry(0, 30, 1500, 1000)