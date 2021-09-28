from PySide6.QtWidgets import (QWidget, QLineEdit, QVBoxLayout, 
                                QPushButton, QLabel, QFileDialog)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt

import os

from src.tools import dirTools


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
            dirTools.ensureDir(os.path.join("data", category))
            image = self.selectedFile
            if image:
                _, file_extension = os.path.splitext(image)
                image_from = open(image, "rb")
                image_to = open(os.path.join("data", ".images" , category) + file_extension, "wb")
                image_to.write(image_from.read())
                image_from.close()
                image_to.close()