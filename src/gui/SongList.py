import os
from PySide6.QtWidgets import (QCheckBox, QHBoxLayout, QWidget, QLineEdit, QVBoxLayout, 
                                QScrollArea, QLabel)
from PySide6.QtCore import Qt

from src.tools import dirTools

from .SongDisplay import ScrollableSongDisplay


class ScrollAndSearchSongList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.setGeometry(0, 0, 400, 1000)
        self.setWindowTitle('Song list')

        self.scrollableSongList = ScrollableSongList()


        self.filterBar = SearchBar(self)


        layout.addWidget(self.filterBar)
        layout.addWidget(self.scrollableSongList)

        self.setLayout(layout)

        self.show()

class SearchBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QHBoxLayout()

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
        self.parent.scrollableSongList.songList.reloadText(filterText, self.checkBox.isChecked())
    def searchInContent(self, detailed = False):
        self.parent.scrollableSongList.songList.reloadText(self.filter.displayText(), detailed)


class ScrollableSongList(QScrollArea):
    def __init__(self):
        super().__init__()
        self.songList = SongList()
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
        self.catSongs = {}
        for cat in cats:
            self.catSongs[cat] = [song[:-4] for song in dirTools.getSongsFromCatDir(cat)]

    def getText(self, filt = None, detailed = False):
        textLines = []
        for cat in self.catSongs.keys():
            catEmpty = True
            textLines.append(f"{cat}")
            for song in self.catSongs[cat]:
                
                linkedTitle = f"{'&nbsp;'*8}<a href=\"{cat}#{song}\">{song}</a>"
                if filt:
                    if filt.lower() in song.lower():
                        textLines.append(linkedTitle)
                        catEmpty = False
                    else:
                        if detailed:
                            with open(os.path.join(os.getcwd(), "data", cat, song + ".sng"), "r") as f:
                                text = f.read()
                                if filt.lower() in text.lower():
                                    textLines.append(linkedTitle)
                                    catEmpty = False
                else:
                    textLines.append(linkedTitle)
                    catEmpty = False
            if catEmpty:
                textLines.pop()
        return "<br>".join(textLines)

