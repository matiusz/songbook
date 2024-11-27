from .Song import Song
from ..tools.loggerSetup import logging
from ..tools.dirTools import getCategoriesFromDirs, getSongFilenamesFromCatDir

logger = logging.getLogger(__name__)

class Songbook:
    def __init__(self):
        self.sb: dict[str, list[Song]] = {}
        for cat in getCategoriesFromDirs():
            self.sb[cat] = [Song.loadFromCatAndTitle(cat, songFilename[:-4]) for songFilename in getSongFilenamesFromCatDir(cat)]
            for song in self.sb[cat]:
                if song.category != cat:
                    logger.warning(f"Category mismatch for song {song.title} - category: {song.category}, folder: {cat}")
