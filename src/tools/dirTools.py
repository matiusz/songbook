import os

from src.obj.Config import config

def isSongCategoryDir(dirname):
    return os.path.isdir(os.path.join(config.dataFolder, dirname)) and not (dirname.startswith((".", "_")))

def ensureFileDir(file_path):
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)

def ensureDir(directory):
    os.makedirs(directory, exist_ok=True)


def getCategoryNames():
    categories = []
    for dirname in os.listdir(config.dataFolder):
        if os.path.isdir(os.path.join(config.dataFolder, dirname)) and not dirname.startswith("."):
            categories.append(dirname)
    return categories


def getSongFilenamesFromCatDir(category):
    songs = []
    for songname in os.listdir(os.path.join(config.dataFolder, category)):
        if songname.endswith(".sng"):
            songs.append(songname)
    return songs
