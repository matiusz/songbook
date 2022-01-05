from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                               QLabel, QMessageBox)
from PySide6.QtGui import QIcon, QPixmap

from src.gui.SongEditor import ScrollableSongEditor
from src.gui.CategoryEditor import NewCategory
from src.gui.SongList import ScrollAndSearchSongList
from src.gui.SongTabs import QSongTabs

from src.tools.openDefault import open_with_default_app
from src.tools import dirTools

from src.obj.Config import config

from src import TeXcompile, songbookTeXmaker

import os


class MainMenu(QWidget):
    def __init__(self, editorMode=False):
        super().__init__()
        self.setWindowTitle('Songbook Maker')

        dirTools.ensureDir(os.path.join(config.dataFolder, config.imageFolder))
        icon = QIcon("guitar.ico")
        self.setWindowIcon(icon)
        label = QLabel()
        image = QPixmap(os.path.join(config.dataFolder, config.appLogo))
        if image:
            label.setPixmap(image)
        else:
            label.setText("Songbook Maker\n<Warning: logo file is missing>")

        if editorMode:
            categoryButton = QPushButton('New Category', self)
            categoryButton.clicked.connect(self.addCategoryField)

            songButton = QPushButton('Song Editor', self)
            songButton.clicked.connect(self.addSongField)

        tabsButton = QPushButton('Show Songs', self)
        tabsButton.clicked.connect(self.tabsSongsField)

        #listButton = QPushButton('Songs List', self)
        #listButton.clicked.connect(self.listSongsField)

        compileButton = QPushButton('Create PDF', self)
        compileButton.clicked.connect(self.generateAndCompileTex)

        layout = QVBoxLayout()
        layout.addWidget(label)
        if editorMode:
            layout.addWidget(categoryButton)
            layout.addWidget(songButton)
        layout.addWidget(tabsButton)
        #layout.addWidget(listButton)
        layout.addWidget(compileButton)
        self.setLayout(layout)
        self.show()

    def generateAndCompileTex(self):
        songbookTexFile = songbookTeXmaker.main()
        try:
            songbookPdfFile = TeXcompile.main()
        except ModuleNotFoundError:
            msgBox = QMessageBox()
            msgBox.setText(
                "Please check if pdflatex is installed or if .tex file was successfully generated.")
            msgBox.exec()
            return
        else:
            open_with_default_app(os.path.join(os.getcwd(), songbookPdfFile))

    def listSongsField(self):
        self.songList = ScrollAndSearchSongList()

    def tabsSongsField(self):
        self.songTabs = QSongTabs()

    def addSongField(self):
        self.currentSong = ScrollableSongEditor()

    def addCategoryField(self):
        self.currentCat = NewCategory()
