from src.obj.Song import Song
import os

def getCategoriesFromDirs(dataFolder) -> list:
        categories = []
        for dirname in os.listdir(dataFolder):
            if os.path.isdir(os.path.join(dataFolder, dirname)) and not dirname.startswith("."):
                categories.append(dirname)
        return categories

def getSongsFromCatDir(dataFolder, category) -> list:
    songs = []
    for songname in os.listdir(os.path.join(dataFolder, category)):
        if songname.endswith(".sng"):
            songs.append(songname[:-4])
    return songs

class Songbook:
    def __init__(self, dataFolder):
        self.sb = {}
        for cat in getCategoriesFromDirs(dataFolder):
            self.sb[cat] = [Song.loadFromCatAndTitle(
                cat, songFilename) for songFilename in getSongsFromCatDir(dataFolder, cat)]
    