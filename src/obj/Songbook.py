from .Song import Song
from src.tools.loggerSetup import logging
from collections import defaultdict
from unidecode import unidecode
from src.tools import fuzz
from string import punctuation
from src.tools.dirTools import getCategoriesFromDirs, getSongFilenamesFromCatDir

logger = logging.getLogger(__name__)

class Songbook:
    def __init__(self):
        self.sb = {}
        for cat in getCategoriesFromDirs():
            self.sb[cat] = [Song.loadFromCatAndTitle(cat, songFilename[:-4]) for songFilename in getSongFilenamesFromCatDir(cat)]
            for song in self.sb[cat]:
                if song.category != cat:
                    logger.warning(f"Category mismatch for song {song.title} - category: {song.category}, folder: {cat}")

    def filteredSongs(self, filter):
        filtered = defaultdict(list)
        for cat, songs in self.sb.items():
            for song in songs:
                print(fuzz.partial_ratio(prepareSearchString(filter), prepareSearchString(song.filterString)))
                print(prepareSearchString(filter))
                print(prepareSearchString(song.filterString))
                if not filter or \
                    prepareSearchString(filter) in prepareSearchString(song.title) or \
                    fuzz.partial_ratio(prepareSearchString(filter), prepareSearchString(song.filterString)) > 90:
                    filtered[cat].append(song)
        return filtered
    
def prepareSearchString(string):
    string = string.lower()
    string = unidecode(string)
    string = string.translate(str.maketrans('', '', punctuation))
    return string