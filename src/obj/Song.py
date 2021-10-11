from __future__ import annotations
import json
import os

from src.obj.Config import config

class Song:
    def __init__(self, title : str, category : str):
        self.title = title
        self.category = category
        self.author :str = None
        self.capo : str = None
        self.sections : SongSection = []
    def addSection(self, section : dict) -> SongSection:
        self.sections.append(section)
        return section

    @property
    def linkedTitle(self) -> str:
        return f"{'&nbsp;'*8}<a href=\"{self.category}#{self.title}\">{self.title}</a>"

    @property
    def filterString(self) -> str:
        songCont = self.title + '\n'
        songCont += self.category + '\n'
        songCont += self.author + '\n'
        for sec in self.sections:
            songCont += sec.lyrics + '\n'
        return songCont

    @staticmethod
    def loadFromDict(songDict : dict) -> Song:
        newSong = Song(songDict['title'], songDict['category'])
        try:
            newSong.author = songDict['author']
        except KeyError:
            newSong.author = ""
        try:
            newSong.capo = songDict['capo']
        except KeyError:
            newSong.capo = ""
        for section in songDict['sections']:
            newSong.addSection(SongSection.loadFromDict(section))
        return newSong

    @staticmethod
    def loadFromFile(filePath : str) -> Song:
        with open(filePath, "rb") as f:
            return Song.loadFromDict(json.loads(f.read()))

    @staticmethod
    def loadFromCatAndTitle(category, title) -> Song:
        with open(os.path.join(config.dataFolder, category, title + ".sng"), "rb") as f:
            return Song.loadFromDict(json.loads(f.read()))

class SongSection:
    def __init__(self, chorus = False):
        self.lyrics = None
        self.chords = None
        self.chorus = chorus
    
    @staticmethod
    def loadFromDict(sectionDict : dict) -> SongSection:
        newSection = SongSection()
        newSection.lyrics = sectionDict['lyrics']
        newSection.chords = sectionDict['chords']
        newSection.chorus = sectionDict['chorus']
        return newSection

if __name__=="__main__":
    song = Song.loadFromFile(os.path.join(os.getcwd(), config.dataFolder, "SDM", "Majka" + ".sng"))
    print(song.title)
    print(song.author)
    print(song.category)
    for section in song.sections:
        print(section.lyrics)
