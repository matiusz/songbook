import os
from PySide6.QtWidgets import (QCheckBox, QHBoxLayout, QWidget, QLineEdit, QVBoxLayout, 
                                QScrollArea, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette

from src.obj.Songbook import Songbook
from src.obj.Song import Song

from src.tools import dirTools

from src.gui.SongDisplay import QScrollableSongDisplay

import json

class ScrollAndSearchSongList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.setGeometry(0, 0, 400, 1000)
        self.setWindowTitle('Song list')
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

        songList = SongList()

        self.scrollableSongList = ScrollableSongList(songList)

        self.filterBar = SearchBar(songList)

        layout.addWidget(self.filterBar)
        layout.addWidget(self.scrollableSongList)

        self.setLayout(layout)

        self.show()

class SearchBar(QWidget):
    def __init__(self, songList):
        super().__init__()
        layout = QHBoxLayout()

        self.songList = songList

        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Search...")
        self.filter.textChanged.connect(self.filt)

        self.desc = QLabel()
        self.desc.setText("Search in contents: ")

        self.checkBox = QCheckBox()
        self.checkBox.stateChanged.connect(self.searchInContent)

        layout.addWidget(self.filter)
        layout.addWidget(self.desc)
        layout.addWidget(self.checkBox)

        self.setLayout(layout)
        
    def filt(self, filterText):
        self.songList.reloadText(filterText, self.checkBox.isChecked())
    def searchInContent(self, detailed = False):
        self.songList.reloadText(self.filter.displayText(), detailed)


class ScrollableSongList(QScrollArea):
    def __init__(self, songList):
        super().__init__()
        self.songList = songList
        self.setWidgetResizable(True)
        self.setWidget(self.songList)

class SongList(QLabel):
    def __init__(self):
        super().__init__()
        self.catSongs = Songbook("data").sb
        
        self.reloadText()
        self.setTextFormat(Qt.RichText)
        self.setAlignment(Qt.AlignTop)
    
        self.linkActivated.connect(self.openSongDisplay)

    def openSongDisplay(self, link):
        cat, _, song = link.partition('#')
        QScrollableSongDisplay(cat, song)

    def reloadText(self, filt : str = "", detailed : bool = False):
        self.setText(self.getText(filt, detailed))

    def getText(self, filt = None, detailed = False):
        textLines = []
        for cat in self.catSongs.keys():
            songs = []
            for song in self.catSongs[cat]:
                if filt:
                    if filt.lower() in song.title.lower():
                        songs.append(song.linkedTitle)
                    elif detailed:
                            if filt.lower() in song.filterString.lower():
                                songs.append(song.linkedTitle)
                else:
                    songs.append(song.linkedTitle)
            if songs:
                textLines.append(f"{cat}")
                textLines.extend(songs)
        return "<br>".join(textLines)

