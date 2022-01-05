from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                                QPushButton,QScrollArea, QLabel)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from src.tools.chordShift import shiftChords

from src.obj.Song import Song

class QScrollableSongDisplay(QScrollArea):
    def __init__(self, category=None, songTitle=None):
        super().__init__()
        self.song = QSong(self)
        self.setWindowTitle(songTitle)
        self.setWidget(self.song)
        self.setWidgetResizable(True)
        if category:
            if songTitle:
                self.song.loadSong(category, songTitle)

class QSong(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent = parent
        self.sections = []
        self.resizeOffset = 0
        self.qSections = []
        layout = QVBoxLayout()

        shiftButtonBox = QHBoxLayout()
        
        pitchDownButton = QPushButton('Shift Down', self)
        pitchDownButton.clicked.connect(self.shiftDown)

        pitchUpButton = QPushButton('Shift Up', self)
        pitchUpButton.clicked.connect(self.shiftUp)

        shiftButtonBox.addWidget(pitchDownButton)
        shiftButtonBox.addWidget(pitchUpButton)

        resizeButtonBox = QHBoxLayout()

        sizeUpButton = QPushButton('Size +', self)
        sizeUpButton.clicked.connect(self.sizeUp)
        
        sizeDownButton = QPushButton('Size -', self)
        sizeDownButton.clicked.connect(self.sizeDown)

        resizeButtonBox.addWidget(sizeDownButton)
        resizeButtonBox.addWidget(sizeUpButton)

        layout.addLayout(resizeButtonBox)

        layout.addLayout(shiftButtonBox)

        self.setLayout(layout)

    def sizeUp(self):
        self.resizeOffset += 1
        self.resizeSections()
    def sizeDown(self):
        self.resizeOffset += -1
        self.resizeSections()
    def resizeSections(self):
        [section.resize(25+self.resizeOffset) for section in self.sections]

    def shiftUp(self):
        self.shiftChords(1)
    def shiftDown(self):
        self.shiftChords(-1)
    def shiftChords(self, diff):
        [section.chords.setText(shiftChords(section.chords.text(), diff)) for section in self.sections]

    def newSection(self, chorus = False, ff = "Times"):
        newSec = QSongSection(chorus, ff)
        self.sections.append(newSec)
        self.layout().addLayout(newSec, 0)
        return newSec
    def addBlankSection(self):
        self.newSection()
    def clearSections(self):
        for i, section in enumerate(self.sections):
            section.setParent(None)
            section.lyrics.deleteLater()
            section.chords.deleteLater()
            section.deleteLater()
        self.sections = []
    def loadSong(self, category, songTitle):
        self.clearSections()
        song = Song.loadFromCatAndTitle(category, songTitle)
        if songTitle:
            song = Song.loadFromCatAndTitle(category, songTitle)
            for section in song.sections:
                sect = self.newSection(chorus=section.chorus)
                sect.lyrics.setText(section.lyrics)
                sect.chords.setText(section.chords)
                self.layout().addSpacing(20)
            self.resizeSections()
        self.layout().addStretch(1)
        self.parent.repaint()

class QSongSection(QHBoxLayout):
    def __init__(self, chorus = False, ff = "Times"):
        super().__init__()
        self.chorus = chorus

        self.font = QFont()
        self.font.setFamily(ff)
        
        self.lyrics = QLabel()
        self.lyrics.setFont(self.font)
        self.lyrics.setTextFormat(Qt.PlainText)
        self.lyrics.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        self.chords = QLabel()
        self.chords.setFont(self.font)
        self.chords.setTextFormat(Qt.PlainText)
        self.chords.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        if self.chorus:
            stretches = (70, 20, 10)
            self.insertStretch(0, stretches[2])
        else:
            stretches = (80, 20)
        
        self.addWidget(self.lyrics, stretches[0])
        self.addWidget(self.chords, stretches[1])
    
    def resize(self, size):
        self.font.setPointSize(size)
        self.lyrics.setFont(self.font)
        self.chords.setFont(self.font)

