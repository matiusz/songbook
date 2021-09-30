import os
from PySide6.QtWidgets import (QCheckBox, QHBoxLayout, QWidget, QLineEdit, QVBoxLayout, 
                                QScrollArea, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette

from src.tools import dirTools

from .SongDisplay import ScrollableSongDisplay

import json

def songContents(songDict):
    songCont = songDict['title'] + '\n'
    songCont += songDict['category'] + '\n'
    try:
        songCont += songDict['author'] + '\n'
    except KeyError:
        pass
    for sec in songDict['sections']:
        songCont += sec['lyrics'] + '\n'
    return songCont
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
        self.loadSongs()
        self.setText(self.getText())
        self.setTextFormat(Qt.RichText)
        self.setAlignment(Qt.AlignTop)
    
        
        self.linkActivated.connect(self.openSongDisplay)

    def openSongDisplay(self, link):
        cat, _, song = link.partition('#')
        ScrollableSongDisplay(cat, song)

    def reloadText(self, filt, detailed = False):
        self.setText(self.getText(filt, detailed))
        pass
    
    def loadSongs(self):
        cats = dirTools.getCategoriesFromDirs()
        self.catSongs = {cat:[song[:-4] for song in dirTools.getSongsFromCatDir(cat)] for cat in cats}

    def getText(self, filt = None, detailed = False):
        textLines = []
        for cat in self.catSongs.keys():
            catSongs = []
            for song in self.catSongs[cat]:
                linkedTitle = f"{'&nbsp;'*8}<a href=\"{cat}#{song}\">{song}</a>"
                if filt:
                    if filt.lower() in song.lower():
                        catSongs.append(linkedTitle)
                    elif detailed:
                            with open(os.path.join(os.getcwd(), "data", cat, song + ".sng"), "rb") as f:
                                jsonSong = json.loads(f.read().decode("utf-8"))
                            if filt.lower() in songContents(jsonSong).lower():
                                catSongs.append(linkedTitle)
                else:
                    catSongs.append(linkedTitle)
            if catSongs:
                textLines.append(f"{cat}")
                textLines.extend(catSongs)
        return "<br>".join(textLines)

