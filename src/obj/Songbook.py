from .Song import Song
from src.tools.loggerSetup import logging
from collections import defaultdict

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
                if filter in song.filterString:
                    filtered[cat].append(song)
        return filtered
    
