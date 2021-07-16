from genericpath import exists
import PySide6.QtWidgets

from PySide6.QtWidgets import (QApplication, QWidget, QLineEdit, 
                                QHBoxLayout, QVBoxLayout, QPlainTextEdit, 
                                QPushButton,QScrollArea, QLayout,  
                                QComboBox, QFileDialog, QLabel)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt

import json

import os

from functools import partial

def ensureFileDir(file_path):
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok = True)

def ensureDir(directory):
    os.makedirs(directory, exist_ok = True)

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
            songs.append(songname)
    return songs


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Songbook Maker')

        label = QLabel()
        image = QPixmap("logo")
        if image:            
            label.setPixmap(image)
        else:
            label.setText("Songbook Maker\n<Warning: Logo.png is missing>")
            
        categoryButton = QPushButton('New Category', self)
        categoryButton.clicked.connect(self.addCategoryField)
        
        songButton = QPushButton('Song Editor', self)
        songButton.clicked.connect(self.addSongField)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(categoryButton)
        layout.addWidget(songButton)
        self.setLayout(layout)
        self.show()

    def addSongField(self):
        self.currentSong = ScrollableSong()
    def addCategoryField(self):
        self.currentCat = NewCategory()


class NewCategory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New Category')
        self.setGeometry(200, 100, 500, 500)

        layout = QVBoxLayout()
        
        self.name = QLineEdit()
        self.name.setPlaceholderText("Category Name")
        layout.addWidget(self.name)

        self.label = QLabel()
        self.label.setText("Choose image for the category")
        layout.addWidget(self.label)

        self.image = QFileDialog()
        self.image.setNameFilter("*.jpg *.png *.bmp")
        self.image.setFileMode(QFileDialog.ExistingFile)
        self.image.fileSelected.connect(lambda: self.updateLabel())
        layout.addWidget(self.image)

        closeButton = QPushButton('Save and Quit', self)
        closeButton.clicked.connect(lambda: self.close())
        layout.addWidget(closeButton)

        self.setLayout(layout)
        self.show()

    def updateLabel(self):
        self.selectedFile = self.image.selectedFiles()[0]
        image = QPixmap(self.selectedFile)
        size = QSize(500, 500)
        image = image.scaled(size, Qt.KeepAspectRatio)
        self.label.setPixmap(image)
    def closeEvent(self, event):
        category = self.name.text()
        if category:
            ensureDir(os.path.join("data", category))
            image = self.selectedFile
            if image:
                _, file_extension = os.path.splitext(image)
                image_from = open(image, "rb")
                image_to = open(os.path.join("data", ".images" , category) + file_extension, "wb")
                image_to.write(image_from.read())
                image_from.close()
                image_to.close()


class ScrollableSong(QScrollArea):
    def __init__(self):
        super().__init__()
        self.song = Song(self)
        self.setGeometry(300, 100, 500, 200)
        self.setWindowTitle('Song Field')
        self.setWidget(self.song)
        self.setWidgetResizable(True)
        self.show()

    def closeEvent(self, event):
        preJSON = self.widget().toJSON()
        if preJSON['title']:
            path = os.path.join("data", preJSON['category'], preJSON['title'] + ".sng")
            ensureFileDir(path)
            f = open(path, "w")
            f.write(json.dumps(preJSON))
        event.accept()


class Song(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setGeometry(300, 100, 500, 100)
        self.setWindowTitle('Song Field')
        self.sections = []

        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SetMinimumSize)
        
        self.catBar = QComboBox()
        self.catBar.addItems(getCategoriesFromDirs())
        self.catBar.currentTextChanged.connect(self.reloadSongs)
        layout.addWidget(self.catBar)

        self.readySongsBar = QComboBox()
        self.readySongsBar.addItem("")
        self.readySongsBar.addItems(getSongsFromCatDir(self.catBar.currentText()))
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
        chorusButton.clicked.connect(partial(self.newSection, chorus = True))
        buttonBox.addWidget(chorusButton)
        
        layout.addLayout(buttonBox)
        
        closeButton = QPushButton('Save and Quit', self)
        closeButton.clicked.connect(lambda: self.parent.close())
        layout.addWidget(closeButton)
        
        self.setLayout(layout)
        self.show()

    def newSection(self, chorus = False):
        newSection = SongSection(chorus = chorus)
        self.sections.append(newSection)
        if len(self.sections)<5:
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
        jsonSong['category'] = self.catBar.currentText()
        jsonSong['sections'] = [section.toJSON() for section in self.sections if section]
        return jsonSong
    def loadSong(self, songFilename):
        if songFilename:
            f = open(os.path.join("data", self.catBar.currentText(), songFilename), "rb")
            jsonSong = json.loads(f.read().decode("utf-8"))
            f.close()
            self.titleBar.setText(jsonSong['title'])
            try:
                self.authorBar.setText(jsonSong['author'])
            except KeyError:
                self.authorBar.setText("")
            try:
                self.capoBar.setText(jsonSong['capo'])
            except KeyError:
                self.capoBar.setText("")
            for i, section in enumerate(self.sections):
                section.setParent(None)
                section.lyrics.deleteLater()
                section.chords.deleteLater()
                section.deleteLater()
            self.sections = []
            for section in jsonSong['sections']:
                sect = self.newSection(chorus=section['chorus'])
                sect.lyrics.setPlainText(section['lyrics'])
                sect.chords.setPlainText(section['chords'])
        else:
            for i, section in enumerate(self.sections):
                section.setParent(None)
                section.lyrics.deleteLater()
                section.chords.deleteLater()
                section.deleteLater()
            self.sections = []
            self.titleBar.setText("")
    def reloadSongs(self):
        self.readySongsBar.clear()
        catSongs = getSongsFromCatDir(self.catBar.currentText())
        self.readySongsBar.addItem("")
        self.readySongsBar.addItems(catSongs)

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

def main():
    import sys
    app = QApplication(sys.argv)
    window = MainMenu()
    ensureDir(os.path.join("data", ".images"))
    try:
        f = open(os.path.join("data", "categories.cfg"), "rb")
    except FileNotFoundError:
        existingCategories = []
    else:
        existingCategories = [line.decode("utf-8").replace("\r", "").replace("\n", "") for line in f.readlines()]
        f.close()
    app.exec()
    f = open(os.path.join("data", "categories.cfg"), "ab")
    for dirname in os.listdir("data"):
        if os.path.isdir(os.path.join("data", dirname)) and not (dirname.startswith(".") or dirname.startswith("_")):
            if dirname not in existingCategories and ("#" + dirname) not in existingCategories:
                f.write((dirname+"\n").encode("utf-8"))
    f.close()

if __name__=="__main__":
    main()
