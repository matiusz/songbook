from src.obj.Song import Song
import os
from src.tools.loggerSetup import logging

from src.tools.dirTools import getCategoryNames, getSongFilenamesFromCatDir

logger = logging.getLogger(__name__)

class Songbook:
    def __init__(self):
        self.sb = {}
        for cat in getCategoryNames():
            self.sb[cat] = [Song.loadFromCatAndTitle(cat, songFilename[:-4]) for songFilename in getSongFilenamesFromCatDir(cat)]
            for song in self.sb[cat]:
                if song.category != cat:
                    logger.warning(f"Category mismatch for song {song.title} - category: {song.category}, folder: {cat}")
    