from PySide6.QtWidgets import QApplication

import json

import os

from src.gui.MainMenu import MainMenu
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

def main():
    import sys
    app = QApplication(sys.argv)
    window = MainMenu()
    dirTools.ensureDir(os.path.join(config.dataFolder, config.imageFolder))
    existingCatsDict = getCatsDict()
    recreateCatDirs(existingCatsDict)
    app.exec()
    existingCatsDict = addMissingCats(existingCatsDict)
    with open(os.path.join(config.dataFolder, config.categoriesFile), "wb") as f:
        f.write(json.dumps(existingCatsDict, indent = 4).encode("utf-8"))
    
if __name__=="__main__":
    main()
