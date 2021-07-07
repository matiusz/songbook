from PySide6.QtWidgets import (QApplication, QWidget, QLineEdit, 
                                QHBoxLayout, QVBoxLayout, QPlainTextEdit, 
                                QPushButton,QScrollArea, QLayout,  
                                QComboBox, QFileDialog, QLabel)

import json

import os

from functools import partial

def ensure_file_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)




class NewCategory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New Category')
        self.setGeometry(200, 100, 500, 500)
        self.name = QLineEdit()
        self.name.setPlaceholderText("Category Name")
        self.label = QLabel()
        self.label.setText("Choose image for the category")
        self.image = QFileDialog()
        self.image.setNameFilter("*.py *.jpg *.png *.bmp")
        layout = QVBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(self.label)
        layout.addWidget(self.image)
        self.setLayout(layout)
        self.show()
    def closeEvent(self, event):
        category = self.name.text()
        if category:
            create_dir(category)
            image = self.image.selectedFiles()[0]
            if image:
                _, file_extension = os.path.splitext(image)
                image_from = open(image, "rb")
                image_to = open(os.path.join(".images" , category) + file_extension, "wb")
                image_to.write(image_from.read())
                image_from.close()
                image_to.close()

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.songs = []
        self.categories = []
        self.setGeometry(100, 100, 200, 150)
        self.setWindowTitle('Songbook Maker')
        songButton = QPushButton('New Song', self)
        songButton.clicked.connect(self.add_song_field)
        songButton.move(50, 50)
        categoryButton = QPushButton('New Category', self)
        categoryButton.clicked.connect(self.add_category_field)
        categoryButton.move(50, 75)
        self.show()
    def add_song_field(self):
        self.songs.append(ScrollableSong())
    def add_category_field(self):
        self.categories.append(NewCategory())
        
        

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
        ensure_file_dir(path)
        f = open(path, "w")
        f.write(json.dumps(preJSON))
        event.accept()

def getCategoriesFromDirs():
    categories = []
    for dirname in os.listdir():
        if os.path.isdir(dirname) and not dirname.startswith("."):
            categories.append(dirname)
    return categories


class Song(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.catBar = QComboBox()
        self.catBar.addItems(getCategoriesFromDirs())
        layout.addWidget(self.catBar)
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
    app.exec()
    f = open("categories.cfg", "wb")
    for dirname in os.listdir():
        if os.path.isdir(dirname) and not dirname.startswith("."):
            f.write((dirname+"\n").encode("utf-8"))
    f.close()