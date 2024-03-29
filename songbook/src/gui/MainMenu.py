from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                               QLabel, QMessageBox)
from PySide6.QtGui import QIcon, QPixmap

from ..gui.SongEditor import ScrollableSongEditor
from ..gui.CategoryEditor import NewCategory
from ..gui.SongTabs import QSongTabs

from ..tools.openDefault import open_with_default_app
from ..tools import dirTools

from ..obj.Config import config

from .. import TeXcompile, songbookTeXmaker

import os


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Songbook Maker')

        dirTools.ensureDir(os.path.join(config.dataFolder, config.imageFolder))
        icon = QIcon("guitar.ico")
        self.setWindowIcon(icon)
        label = QLabel()
        image = QPixmap(config.appLogo)
        if image:
            label.setPixmap(image)
        else:
            label.setText("Songbook Maker\n<Warning: logo file is missing>")

        categoryButton = QPushButton('New Category', self)
        categoryButton.clicked.connect(self.addCategoryField)

        songButton = QPushButton('Song Editor', self)
        songButton.clicked.connect(self.addSongField)

        tabsButton = QPushButton('Song Display', self)
        tabsButton.clicked.connect(self.tabsSongsField)

        compileButton = QPushButton('Create PDF', self)
        compileButton.clicked.connect(self.generateAndCompileTex)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(categoryButton)
        layout.addWidget(songButton)
        layout.addWidget(tabsButton)
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
        else:
            open_with_default_app(os.path.join(os.getcwd(), songbookPdfFile))

    def tabsSongsField(self):
        self.songTabs = QSongTabs()

    def addSongField(self):
        self.currentSong = ScrollableSongEditor()

    def addCategoryField(self):
        self.currentCat = NewCategory()
