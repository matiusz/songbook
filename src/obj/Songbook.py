from .Song import Song
import os


class Songbook:
    def __init__(self, dataFolder):
        self.sb = {}
        for cat in Songbook.getCategoriesFromDirs(dataFolder):
            self.sb[cat] = [Song.loadFromCatAndTitle(
                cat, songFilename) for songFilename in Songbook.getSongsFromCatDir(dataFolder, cat)]

    @staticmethod
    def getCategoriesFromDirs(dataFolder) -> list:
        categories = []
        for dirname in os.listdir(dataFolder):
            if os.path.isdir(os.path.join(dataFolder, dirname)) and not dirname.startswith("."):
                categories.append(dirname)
        return categories

    @staticmethod
    def getSongsFromCatDir(dataFolder, category) -> list:
        songs = []
        for songname in os.listdir(os.path.join(dataFolder, category)):
            if songname.endswith(".sng"):
                songs.append(songname[:-4])
        return songs
