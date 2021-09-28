from PySide6.QtWidgets import QApplication

import json

import os

from src.gui.MainMenu import MainMenu
from src.tools import dirTools

def getCatsDict():
    try:
        with open(os.path.join("data", "categories.cfg"), "rb") as catConfig:
            return json.loads(catConfig.read())
    except FileNotFoundError:
       return {}

def recreateCatDirs(catDict):
    [dirTools.ensureDir(os.path.join("data", cat)) for cat in catDict.keys()]

def addMissingCats(catDict):
    for dirname in os.listdir("data"):
                if os.path.isdir(os.path.join("data", dirname)) and not (dirname.startswith(".") or dirname.startswith("_")):
                    if dirname not in catDict.keys():
                        catDict[dirname] = dirname
    return catDict

def main():
    import sys
    app = QApplication(sys.argv)
    window = MainMenu()
    dirTools.ensureDir(os.path.join("data", ".images"))
    existingCatsDict = getCatsDict()
    recreateCatDirs(existingCatsDict)
    app.exec()
    existingCatsDict = addMissingCats(existingCatsDict)
    with open(os.path.join("data", "categories.cfg"), "wb") as f:
        f.write(json.dumps(existingCatsDict, indent = 4).encode("utf-8"))
    
if __name__=="__main__":
    main()
