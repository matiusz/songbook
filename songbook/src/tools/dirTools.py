import os

from ..obj.Config import config

def isSongCategoryDir(dirname):
    return os.path.isdir(os.path.join(config.dataFolder, dirname)) and not (dirname.startswith((".", "_")))

def ensureFileDir(file_path: str):
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)


def ensureDir(directory: str):
    os.makedirs(directory, exist_ok=True)


def getCategoriesFromDirs() -> list[str]:
    '''Returns a list of directories contained in the data folder defined in config that do not start with "."'''
    categories = []
    for dirname in os.listdir(config.dataFolder):
        if os.path.isdir(os.path.join(config.dataFolder, dirname)) and not dirname.startswith("."):
            categories.append(dirname)
    return categories



def getSongFilenamesFromCatDir(category: str) -> list[str]:
    '''Returns all .sng files from a specified category within data folder defined in config'''
    songs = []
    for songname in os.listdir(os.path.join(config.dataFolder, category)):
        if songname.endswith(".sng"):
            songs.append(songname)
    return songs
