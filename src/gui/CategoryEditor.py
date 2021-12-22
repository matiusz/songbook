from PySide6.QtWidgets import (QWidget, QLineEdit, QVBoxLayout, 
                                QPushButton, QLabel, QFileDialog)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt

import os, json

from src.tools import dirTools

from src.obj.Config import config

def getCatsDict():
    try:
        with open(os.path.join(config.dataFolder, config.categoriesFile), "rb") as catConfig:
            return json.loads(catConfig.read())
    except FileNotFoundError:
       return {}

def recreateCatDirs(catDict):
    [dirTools.ensureDir(os.path.join(config.dataFolder, cat)) for cat in catDict.keys()]

def addMissingCats(catDict):
    for dirname in os.listdir(config.dataFolder):
                if os.path.isdir(os.path.join(config.dataFolder, dirname)) and not (dirname.startswith(".") or dirname.startswith("_")):
                    if dirname not in catDict.keys():
                        catDict[dirname] = dirname
    return catDict

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
        self.image.setNameFilter("*.jpg *.png *.bmp *.tiff *.tif *.jpeg")
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
            dirTools.ensureDir(os.path.join(config.dataFolder, category))
            image = self.selectedFile
            if image:
                _, file_extension = os.path.splitext(image)
                image_from = open(image, "rb")
                image_to = open(os.path.join(config.dataFolder, config.imageFolder , category) + file_extension, "wb")
                image_to.write(image_from.read())
                image_from.close()
                image_to.close()
        existingCatsDict = getCatsDict()
        recreateCatDirs(existingCatsDict)
        existingCatsDict = addMissingCats(existingCatsDict)
        with open(os.path.join(config.dataFolder, config.categoriesFile), "wb") as f:
            f.write(json.dumps(existingCatsDict, indent = 4).encode("utf-8"))