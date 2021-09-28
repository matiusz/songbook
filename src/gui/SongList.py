from PySide6.QtWidgets import (QWidget, QLineEdit, QVBoxLayout, 
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

        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Search...")
        self.filter.textChanged.connect(self.scrollableSongList.songList.reloadText)


        layout.addWidget(self.filter)
        layout.addWidget(self.scrollableSongList)

        self.setLayout(layout)

        self.show()

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

    def reloadText(self, filt):
        self.setText(self.getText(filt))
        pass
    
    def loadSongs(self):
        cats = dirTools.getCategoriesFromDirs()
        self.catSongs = {}
        for cat in cats:
            self.catSongs[cat] = [song[:-4] for song in dirTools.getSongsFromCatDir(cat)]

    def getText(self, filt = None):
        textLines = []
        for cat in self.catSongs.keys():
            catEmpty = True
            textLines.append(f"{cat}")
            for song in self.catSongs[cat]:
                if filt:
                    if filt.lower() in song.lower():
                        textLines.append(f"{'&nbsp;'*8}<a href=\"{cat}#{song}\">{song}</a>")
                        catEmpty = False
                else:
                    textLines.append(f"{'&nbsp;'*8}<a href=\"{cat}#{song}\">{song}</a>")
                    catEmpty = False
            if catEmpty:
                textLines.pop()
        return "<br>".join(textLines)

