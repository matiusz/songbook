from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                                QPushButton,QScrollArea, QLabel)
from PySide6.QtGui import QPalette, QFont
from PySide6.QtCore import Qt

import json

import os

from src.tools.chordShift import shiftChords

class ScrollableSongDisplay(QScrollArea):
    def __init__(self, category=None, songTitle=None):
        super().__init__()
        self.song = Song(self)
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)
        self.setGeometry(400, 50, 700, 900)
        self.setWindowTitle(songTitle)
        self.setWidget(self.song)
        self.setWidgetResizable(True)
        self.show()
        if category:
            if songTitle:
                self.song.loadSong(category, songTitle)

class Song(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.resizeFactor = 1
        self.sections = []
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
        self.show()

    def sizeUp(self):
        self.resizeFactor += 0.1
        self.resizeSections()
    def sizeDown(self):
        self.resizeFactor += -0.1
        self.resizeSections()
    def resizeSections(self):
        [section.resize(15*self.resizeFactor) for section in self.sections]

    def shiftUp(self):
        self.shiftChords(1)
    def shiftDown(self):
        self.shiftChords(-1)
    def shiftChords(self, diff):
        for i, section in enumerate(self.sections):
            section.chords.setText(shiftChords(section.chords.text(), diff))

    def newSection(self, chorus = False, ff = "Times"):
        newSec = SongSection(chorus, ff)
        self.sections.append(newSec)
        if len(self.sections)<5:
            self.parent.setMinimumHeight(self.minimumSize().height()+110)
        self.layout().addLayout(newSec)
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
    def loadSong(self, category, songFilename):
        self.clearSections()
        if songFilename:
            with open(os.path.join("data", category, songFilename + ".sng"), "rb") as f:
                jsonSong = json.loads(f.read().decode("utf-8"))
            for section in jsonSong['sections']:
                sect = self.newSection(chorus=section['chorus'])
                sect.lyrics.setText(section['lyrics'])
                sect.chords.setText(section['chords'])
                self.addBlankSection()
            self.resizeSections()
        self.parent.repaint()

class SongSection(QHBoxLayout):
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

