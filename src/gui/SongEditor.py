from shutil import ExecError
from PySide6.QtWidgets import (QWidget, QLineEdit,
                               QHBoxLayout, QVBoxLayout, QPlainTextEdit,
                               QPushButton, QScrollArea, QLayout,
                               QComboBox, QApplication)

import json

import os

from functools import partial
from src.obj.Song import Song

from src.tools import dirTools

from src.obj.Config import config


class ScrollableSongEditor(QScrollArea):
    def __init__(self):
        super().__init__()
        self.song = QSong(self)
        self.setGeometry(300, 100, 500, 200)
        self.setWindowTitle('Song Field')
        self.setWidget(self.song)
        self.setWidgetResizable(True)
        self.show()

    def saveSong(self):
        Song.loadFromDict(self.song.toJSON()).save()
        self.song.reloadSongs()

    def closeEvent(self, event):
        # self.saveSong()
        event.accept()


class QSong(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setGeometry(300, 100, 500, 100)
        self.setWindowTitle('Song Field')
        self.sections = []

        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SetMinimumSize)

        self.changeCatBar = QComboBox()
        self.changeCatBar.addItem("Change Category")
        self.changeCatBar.addItems(dirTools.getCategoriesFromDirs())
        layout.addWidget(self.changeCatBar)

        self.catBar = QComboBox()
        self.catBar.addItems(dirTools.getCategoriesFromDirs())
        self.catBar.currentTextChanged.connect(self.reloadSongs)
        layout.addWidget(self.catBar)

        self.readySongsBar = QComboBox()
        self.readySongsBar.addItem("")
        self.readySongsBar.addItems(
            dirTools.getSongFilenamesFromCatDir(self.catBar.currentText()))
        self.readySongsBar.currentTextChanged.connect(self.loadSong)
        layout.addWidget(self.readySongsBar)

        self.titleBar = QLineEdit()
        self.titleBar.setPlaceholderText("Song Title")
        layout.addWidget(self.titleBar)

        self.authorBar = QLineEdit()
        self.authorBar.setPlaceholderText("Song Authors")
        layout.addWidget(self.authorBar)

        self.capoBar = QLineEdit()
        self.capoBar.setPlaceholderText("Capo")
        layout.addWidget(self.capoBar)

        buttonBox = QHBoxLayout()

        verseButton = QPushButton('New Verse', self)
        verseButton.clicked.connect(self.newSection)
        buttonBox.addWidget(verseButton)

        chorusButton = QPushButton('New Chorus', self)
        chorusButton.clicked.connect(partial(self.newSection, chorus=True))
        buttonBox.addWidget(chorusButton)

        layout.addLayout(buttonBox)

        closeButton = QPushButton('Quit', self)
        closeButton.clicked.connect(lambda: self.parent.close())
        layout.addWidget(closeButton)

        saveButton = QPushButton('Save', self)
        saveButton.clicked.connect(lambda: self.parent.saveSong())
        layout.addWidget(saveButton)

        self.setLayout(layout)
        self.show()

    def newSection(self, chorus=False):
        newSection = QSongSection(chorus=chorus)
        self.sections.append(newSection)
        if len(self.sections) < 5:
            self.parent.setMinimumHeight(self.minimumSize().height()+110)
        self.layout().addLayout(newSection)
        return newSection

    def toJSON(self):
        jsonSong = {}
        jsonSong['title'] = self.titleBar.text()
        if author := self.authorBar.text():
            jsonSong["author"] = author
        if capo := self.capoBar.text():
            jsonSong['capo'] = capo
        if (newCat := self.changeCatBar.currentText()) != "Change Category":
            jsonSong["category"] = newCat
            try:
                os.remove(os.path.join(config.dataFolder,
                        self.catBar.currentText(), self.titleBar.text() + ".sng"))
            except FileNotFoundError:
                pass
        else:
            jsonSong['category'] = self.catBar.currentText()
        jsonSong['sections'] = [section.toJSON()
                                for section in self.sections if section]
        return jsonSong

    def loadSong(self, songFilename):
        if songFilename:
            song = Song.loadFromFile(os.path.join(
                config.dataFolder, self.catBar.currentText(), songFilename))
            self.titleBar.setText(song.title)
            self.authorBar.setText(song.author or '')
            self.capoBar.setText(song.capo or '')
            for i, section in enumerate(self.sections):
                section.setParent(None)
                section.lyrics.deleteLater()
                section.chords.deleteLater()
                section.deleteLater()
            self.sections = []
            for section in song.sections:
                sect = self.newSection(chorus=section.chorus)
                sect.lyrics.setPlainText(section.lyrics)
                sect.chords.setPlainText(section.chords)
        else:
            for i, section in enumerate(self.sections):
                section.setParent(None)
                section.lyrics.deleteLater()
                section.chords.deleteLater()
                section.deleteLater()
            self.sections = []
            self.titleBar.setText("")
            self.authorBar.setText("")
            self.capoBar.setText("")

    def reloadSongs(self):
        self.changeCatBar.setCurrentText("Change Category")
        self.readySongsBar.clear()
        catSongs = dirTools.getSongFilenamesFromCatDir(self.catBar.currentText())
        self.readySongsBar.addItem("")
        self.readySongsBar.addItems(catSongs)


class QSongSection(QHBoxLayout):
    def __init__(self, chorus=False):
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

    def __bool__(self):
        if self.chords.toPlainText() or self.lyrics.toPlainText():
            return True
        else:
            return False

    def toJSON(self):
        jsonSection = {}
        jsonSection['chords'] = self.chords.toPlainText()
        jsonSection['lyrics'] = self.lyrics.toPlainText()
        jsonSection['chorus'] = self.chorus
        return jsonSection
