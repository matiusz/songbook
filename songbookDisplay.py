import PySide6.QtWidgets

from PySide6.QtWidgets import (QApplication, QWidget, QLineEdit, 
                                QHBoxLayout, QVBoxLayout, QPlainTextEdit, 
                                QPushButton,QScrollArea, QLayout,  
                                QComboBox, QFileDialog, QLabel)
from PySide6.QtGui import QPalette, QPixmap, QFont
from PySide6.QtCore import QSize, Qt

import json

import os

from functools import partial

from chordShift import shiftChords

def getCategoriesFromDirs():
    categories = []
    for dirname in os.listdir("data"):
        if os.path.isdir(os.path.join("data", dirname)) and not dirname.startswith("."):
            categories.append(dirname)
    return categories

def getSongsFromCatDir(category):
    songs = []
    for songname in os.listdir(os.path.join("data", category)):
        if songname.endswith(".sng"):
            songs.append(songname[:-4])
    return songs



class ScrollableSong(QScrollArea):
    def __init__(self):
        super().__init__()
        self.song = Song(self)
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)
        self.setGeometry(300, 100, 500, 200)
        self.setWindowTitle('Song Field')
        self.setWidget(self.song)
        self.setWidgetResizable(True)
        self.show()

class Song(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.resizeFactor = 1
        self.setGeometry(300, 100, 500, 100)
        self.setWindowTitle('Song Field')
        self.sections = []
        self.shift = 0
        layout = QVBoxLayout()
        #layout.setSizeConstraint(QLayout.SetMinimumSize)
        
        self.catBar = QComboBox()
        self.catBar.addItems(getCategoriesFromDirs())
        self.catBar.currentTextChanged.connect(self.reloadSongs)
        layout.addWidget(self.catBar)

        self.readySongsBar = QComboBox()
        self.readySongsBar.addItem("")
        self.readySongsBar.addItems(getSongsFromCatDir(self.catBar.currentText()))
        self.readySongsBar.currentTextChanged.connect(self.loadSong)

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

        layout.addWidget(self.readySongsBar)

        layout.addLayout(resizeButtonBox)

        layout.addLayout(shiftButtonBox)


        self.setLayout(layout)
        self.show()
    def updateChords(self):
        for i, section in enumerate(self.sections):
            section.chords.setText(shiftChords(section.chords.text(), self.shift))
    def sizeUp(self):
        self.resizeFactor += 0.1
        self.resizeSections()
    def sizeDown(self):
        self.resizeFactor += -0.1
        self.resizeSections()
    def resizeSections(self):
        font = QFont("Times", 10*self.resizeFactor)
        for i, section in enumerate(self.sections):
            section.lyrics.setFont(font)
            section.chords.setFont(font)
    def shiftUp(self):
        self.shift = 1
        self.updateChords()
    def shiftDown(self):
        self.shift = -1
        self.updateChords()
    def newSection(self, chorus = False):
        newSection = SongSection(chorus = chorus)
        self.sections.append(newSection)
        if len(self.sections)<5:
            self.parent.setMinimumHeight(self.minimumSize().height()+110)
        self.layout().addLayout(newSection)
        return newSection
    def loadSong(self, songFilename):
        self.shift = 0
        if songFilename:
            f = open(os.path.join("data", self.catBar.currentText(), songFilename + ".sng"), "rb")
            jsonSong = json.loads(f.read().decode("utf-8"))
            f.close()
            for i, section in enumerate(self.sections):
                section.setParent(None)
                section.lyrics.deleteLater()
                section.chords.deleteLater()
                section.deleteLater()
            self.sections = []
            for section in jsonSong['sections']:
                sect = self.newSection(chorus=section['chorus'])
                sect.lyrics.setText(section['lyrics'])
                sect.chords.setText(shiftChords(section['chords'], self.shift))
            self.resizeSections()
            self.parent.setGeometry(300, 100, 500*self.resizeFactor, 600*self.resizeFactor)
            self.parent.repaint()
        else:
            for i, section in enumerate(self.sections):
                section.setParent(None)
                section.lyrics.deleteLater()
                section.chords.deleteLater()
                section.deleteLater()
            self.sections = []
            self.parent.setGeometry(300, 100, 500, 200)
            self.parent.repaint()
    def reloadSongs(self):
        self.readySongsBar.clear()
        catSongs = getSongsFromCatDir(self.catBar.currentText())
        self.readySongsBar.addItem("")
        self.readySongsBar.addItems(catSongs)
        #self.parent.setGeometry(300, 100, 500, 200)
        #self.parent.repaint()

class SongSection(QHBoxLayout):
    def __init__(self, chorus = False):
        super().__init__()
        #self.addStrut(90)
        self.chorus = chorus
        self.lyrics = QLabel()
        font = QFont()
        self.lyrics.setFont(font)
        self.lyrics.setTextFormat(Qt.PlainText)
        self.lyrics.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.chords = QLabel()
        self.chords.setFont(font)
        self.chords.setTextFormat(Qt.PlainText)
        self.chords.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        if self.chorus:
            stretches = (70, 20, 10)
            self.insertStretch(0, stretches[2])
        else:
            stretches = (80, 20)
        self.addWidget(self.lyrics, stretches[0])
        self.addWidget(self.chords, stretches[1])

def main():
    import sys
    app = QApplication(sys.argv)
    window = ScrollableSong()
    app.exec()

if __name__=="__main__":
    main()
