from __future__ import annotations
import os
import itertools
import re

from src.obj.Config import config


class Song:
    def __init__(self, title: str, category: str):
        self.title = title
        self.category = category
        self.author: str = None
        self.capo: str = None
        self.sections: SongSection = []

    def addSection(self, section: dict) -> SongSection:
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

    def serialize(self) -> str:
        result = \
            f"#title {self.title}\n" + \
            f"#author {self.author}\n" + \
            f"#category {self.category}\n" + \
            (f"#capo {self.capo}\n" if self.capo else '') + \
            "\n"

        for section in self.sections:
            result += "#chorus\n" if section.chorus else "#verse\n"
            for (lyrics, chords) in itertools.zip_longest(section.lyrics.split('\n'), section.chords.split('\n')):
                result += (lyrics if lyrics else '') + \
                    (' ' if lyrics and chords else '') + \
                    ("~ " + chords if chords else '') + '\n'
            result += "\n"

        return result

    def save(self) -> None:
        with open(os.path.join(config.dataFolder, self.category, self.title + ".sng"), "w", encoding='utf-8') as f:
            return f.write(self.serialize())

    @classmethod
    def parse(cls, str) -> Song:
        commands = "title|author|category|capo|chorus|verse"
        dict = {'sections': []}
        # finds all occurences of #command, followed by blank, until another #command or the end
        for (cmd, val) in re.findall(f"^#({commands})(?:\n|\s)((?:.|\n)*?(?=#(?:{commands})|\Z))", str, flags=re.MULTILINE):
            if cmd in ["verse", "chorus"]:
                split_lines = [line.split("~ ") + ['']
                               for line in val.strip().split('\n')]
                (lyrics, chords) = zip(
                    *[(line[0].rstrip(), line[1]) for line in split_lines])
                dict['sections'].append({
                    'lyrics': "\n".join(lyrics),
                    'chords': "\n".join(chords),
                    'chorus': cmd == 'chorus'
                })
            else:
                dict[cmd] = val.strip()
        return cls.loadFromDict(dict)

    @classmethod
    def loadFromDict(cls, songDict: dict) -> Song:
        newSong = cls(songDict['title'], songDict['category'])
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

    @classmethod
    def loadFromFile(cls, filePath: str) -> Song:
        with open(filePath, "r", encoding='utf-8') as f:
            return cls.parse(f.read())

    @classmethod
    def loadFromCatAndTitle(cls, category, title) -> Song:
        return cls.loadFromFile(os.path.join(
            config.dataFolder, category, title + ".sng"))


class SongSection:
    def __init__(self, chorus=False):
        self.lyrics = None
        self.chords = None
        self.chorus = chorus

    @classmethod
    def loadFromDict(cls, sectionDict: dict) -> SongSection:
        newSection = cls()
        newSection.lyrics = sectionDict['lyrics']
        newSection.chords = sectionDict['chords']
        newSection.chorus = sectionDict['chorus']
        return newSection
