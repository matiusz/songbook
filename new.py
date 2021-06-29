from PySide6.QtWidgets import (QApplication, QWidget, QLineEdit, 
                                QHBoxLayout, QVBoxLayout, QPlainTextEdit, 
                                QPushButton, QTableWidget, QSpacerItem, 
                                QScrollArea, QLayout, QSizePolicy)
from PySide6.QtCore import Slot, QSize

import json

from functools import partial

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.songs = []
        btn = QPushButton('New Song', self)
        btn.clicked.connect(self.add_song_field)
        #btn_quit.resize(btn_quit.sizeHint())
        btn.move(75, 50)
        self.setGeometry(100, 100, 200, 150)
        self.setWindowTitle('Window Example')
        self.show()
    def add_song_field(self):
        self.songs.append(ScrollableSong())

class ScrollableSong(QScrollArea):
    def __init__(self):
        super().__init__()
        self.song = Song(self)
        self.setGeometry(300, 100, 500, 100)
        #self.setMinimumWidth(500)
        self.setWindowTitle('Song Field')
        self.setWidget(self.song)
        self.setWidgetResizable(True)
        self.show()
    def closeEvent(self, event):
        dum = json.dumps(self.widget().toJSON())
        print(dum)
        json.loads(dum)
        event.accept()


class Song(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.titleBar = QLineEdit()
        self.titleBar.setPlaceholderText("Song Title")
        layout.addWidget(self.titleBar)
        btnVerse = QPushButton('New Verse', self)
        btnVerse.clicked.connect(lambda: self.newSection())
        btnChorus = QPushButton('New Chorus', self)
        btnChorus.clicked.connect(lambda: self.newSection(chorus = True))
        btnClose = QPushButton('Save&Quit', self)
        btnClose.clicked.connect(lambda: self.parent.close())
        #btn_quit.resize(btn_quit.sizeHint())
        buttonBox = QHBoxLayout()
        buttonBox.addWidget(btnVerse)
        buttonBox.addWidget(btnChorus)
        layout.addLayout(buttonBox)
        layout.addWidget(btnClose)
        self.setGeometry(300, 100, 500, 100)
        self.setWindowTitle('Song Field')
        self.sections = []
        self.setLayout(layout)
        self.show()
    def newSection(self, chorus = False):
        newSection = SongSection(chorus = chorus)
        self.sections.append(newSection)
        if len(self.sections)<5:
            self.parent.setMinimumHeight(self.minimumSize().height()+110)
        self.layout().addLayout(newSection)
    def toJSON(self):
        jsonSong = {}
        jsonSong['title'] = self.titleBar.text()
        jsonSong['sections'] = [section.toJSON() for section in self.sections]
        return jsonSong





class SongSection(QHBoxLayout):
    def __init__(self, chorus = False):
        super().__init__()
        self.addStrut(90)
        self.chorus = chorus
        self.lyrics = QPlainTextEdit()
        self.chords = QPlainTextEdit()
        self.chords.setPlaceholderText("Chords")
        if self.chorus:
            self.lyrics.setPlaceholderText("Chorus lyrics")
            stretches = (70, 25, 5)
            self.insertStretch(0, stretches[2])
        else:
            self.lyrics.setPlaceholderText("Verse lyrics")
            stretches = (75, 25)
        self.addWidget(self.lyrics, stretches[0])
        self.addWidget(self.chords, stretches[1])
    def toJSON(self):
        jsonSection = {}
        jsonSection['chords'] = self.chords.toPlainText()
        jsonSection['lyrics'] = self.lyrics.toPlainText()
        jsonSection['chorus'] = self.chorus
        return jsonSection

# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainMenu()


#window.show()  # IMPORTANT!!!!! Windows are hidden by default.


# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.``