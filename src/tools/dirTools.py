import os
import sys

from src.obj.Config import config

def ensureFileDir(file_path):
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok = True)

def ensureDir(directory):
    os.makedirs(directory, exist_ok = True)

def getCategoriesFromDirs():
    categories = []
    for dirname in os.listdir(config.dataFolder):
        if os.path.isdir(os.path.join(config.dataFolder, dirname)) and not dirname.startswith("."):
            categories.append(dirname)
    return categories

def getSongsFromCatDir(category):
    songs = []
    for songname in os.listdir(os.path.join(config.dataFolder, category)):
        if songname.endswith(".sng"):
            songs.append(songname)
    return songs

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)