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
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def getCategoriesFromDirs():
    categories = []
    for dirname in os.listdir():
        if os.path.isdir(dirname) and not dirname.startswith("."):
            categories.append(dirname)
    return categories


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Songbook Maker')

        image = QPixmap("logo")
        label = QLabel()
        label.setPixmap(image)

        categoryButton = QPushButton('New Category', self)
        categoryButton.clicked.connect(self.addCategoryField)
        
        songButton = QPushButton('New Song', self)
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

        closeButton = QPushButton('Save&Quit', self)
        closeButton.clicked.connect(lambda: self.close())
        layout.addWidget(closeButton)

        self.setLayout(layout)
        self.show()

    def updateLabel(self):
        image = QPixmap(self.image.selectedFiles()[0])
        size = QSize(500, 500)
        image = image.scaled(size, Qt.KeepAspectRatio)
        self.label.setPixmap(image)
    def closeEvent(self, event):
        category = self.name.text()
        if category:
            ensureDir(category)
            image = self.image.selectedFiles()[0]
            if image:
                _, file_extension = os.path.splitext(image)
                image_from = open(image, "rb")
                image_to = open(os.path.join(".images" , category) + file_extension, "wb")
                image_to.write(image_from.read())
                image_from.close()
                image_to.close()


class ScrollableSong(QScrollArea):
    def __init__(self):
        super().__init__()
        self.song = Song(self)
        self.setGeometry(300, 100, 500, 100)
        self.setWindowTitle('Song Field')
        self.setWidget(self.song)
        self.setWidgetResizable(True)
        self.show()

    def closeEvent(self, event):
        preJSON = self.widget().toJSON()
        path = os.path.join(preJSON['category'], preJSON['title'] + ".sng")
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
        layout.addWidget(self.catBar)
        
        self.titleBar = QLineEdit()
        self.titleBar.setPlaceholderText("Song Title")
        layout.addWidget(self.titleBar)
        
        buttonBox = QHBoxLayout()
        
        verseButton = QPushButton('New Verse', self)
        verseButton.clicked.connect(self.newSection)
        buttonBox.addWidget(verseButton)
        
        chorusButton = QPushButton('New Chorus', self)
        chorusButton.clicked.connect(partial(self.newSection, chorus = True))
        buttonBox.addWidget(chorusButton)
        
        layout.addLayout(buttonBox)
        
        closeButton = QPushButton('Save&Quit', self)
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
    def toJSON(self):
        jsonSong = {}
        jsonSong['title'] = self.titleBar.text()
        jsonSong['category'] = self.catBar.currentText()
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

if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainMenu()
    ensureDir(".images")
    app.exec()
    f = open("categories.cfg", "wb")
    for dirname in os.listdir():
        if os.path.isdir(dirname) and not dirname.startswith("."):
            f.write((dirname+"\n").encode("utf-8"))
    f.close()