import os
import json
import re

from src.tools.plAlphabetSort import plSortKey
import asyncio
import aiofiles

from src import headerconfig as headerconfig

from src.tools.chordShift import shiftChords
from src.tools.codings import enUTF8, deUTF8

from src.obj.Config import config
from src.obj.Song import Song

from src.tools.loggerSetup import logging

logger = logging.getLogger(__name__)



def isSongCategoryDir(dirname):
    return os.path.isdir(os.path.join(config.dataFolder, dirname)) and not (dirname.startswith((".", "_")))


async def gatherAllCategories(sem):
    logger.debug(f"Starting loading songs...")
    tasks = [gatherSongs(os.path.join(config.dataFolder, dirname), sem)
             for dirname in os.listdir(config.dataFolder) if isSongCategoryDir(dirname)]
    categories = await asyncio.gather(*tasks)
    logger.info(f"All songs successfully loaded")
    return categories


async def gatherSongs(dirpath, sem):
    logger.debug(f"Loading songs from {dirpath}")
    tasks = [semaphoredLoadSong(dirpath, filename, sem) for filename in os.listdir(
        dirpath) if filename.endswith(".sng")]
    songs = await asyncio.gather(*tasks)
    return songs


async def semaphoredLoadSong(dirpath, filename, sem):
    logger.debug(f"Loading song from {filename} at {dirpath}")
    async with sem:
        return await TexSong.load(os.path.join(dirpath, filename))


class CategoryDict(dict):
    def __missing__(self, key):
        res = self[key] = TexCategory(key)
        return res


class TexCategory:
    def __init__(self, name):
        self.songs = {}
        self.name = name

    def setCatMapping(self, catsDict):
        self.catMap = catsDict

    @property
    def tex(self):
        try:
            name = self.catMap[self.name]
        except (KeyError, AttributeError):
            name = self.name
        catStr = ""
        if config.canvas.sides == "twoside":
            catStr += "\\cleardoublepage\n"
        catStr += f"\\chapter*{{\\centering {name}}}\n" + \
            f"\\addcontentsline{{toc}}{{chapter}}{{{name}}}\n" + \
            f"{{\\centering \\includegraphics[width=\\textwidth,height=0.75\\textheight,keepaspectratio]{{{self.name}}} \\par}}\n"
        catStr += "\\newpage\n"
        return catStr


class TexSong:
    @staticmethod
    async def load(filepath):
        async with aiofiles.open(filepath, "r", encoding='utf-8') as songFile:
            texSong = TexSong(await songFile.read())
        return texSong

    def __init__(self, songData):
        self.song = Song.parse(songData)
        self.title = self.song.title
        self.category = self.song.category

    @property
    def tex(self):
        songStr = f"\\section*{{{self.title}}}\n\\addcontentsline{{toc}}{{section}}{{{self.title}}}\n\\columnratio{{0.78,0.22}}\n\\rmfamily\\raggedbottom"
        author = self.song.author
        if author:
            songStr += f"\\begin{{flushright}}\n{author}\n\\end{{flushright}}"
        capo = self.song.capo
        if capo:
            songStr += f"\\begin{{flushright}}\n{capo}\n\\end{{flushright}}"
        songStr += "\\begin{paracol}{2}\n"
        sections = [self.convertSection(section)
                    for section in self.song.sections]
        if len(sections) > 2:
            sections[-2] = self.convertSection(
                self.song.sections[-2], additionalVspace=sections[-1][1]+1)
            sections[-1] = self.convertSection(
                self.song.sections[-1], additionalVspace=0)
        for section in sections:
            songStr += section[0]
        songStr += "\\end{paracol}\n"
        songStr += "\\newpage\n"
        return songStr

    def superscriptSpecialChars(self, text):
        specialChars = ["1", "2", "3", "4", "5", "6", "7",
                        "8", "9", "0", "+", "-", "*", "sus", "add", "/"]
        chDict = {ch: f"\\textsuperscript{{{ch}}}" for ch in specialChars}
        pattern = re.compile('|'.join(
            sorted([re.escape(key) for key in chDict.keys()], key=len, reverse=True)))
        result = pattern.sub(lambda x: chDict[x.group()], text)
        return result

    def convertSection(self, section, additionalVspace=2):
        chordShift = config.chordShift
        lyrics, l1 = self.convertLineBreaks(section.lyrics)
        if section.chords:
            chords, l2 = self.convertLineBreaks(shiftChords(
                section.chords, chordShift).replace("\\", "\\textbackslash "), chords=True)
        else:
            chords, l2 = "", 0
        vspace = max(l1, l2)
        songStr = f"\n\\ensurevspace{{{vspace+additionalVspace}\\baselineskip}}\n"
        songStr += "\\begin{leftcolumn*} "
        songStr += "\\noindent"
        if section.chorus:
            lyrics = self.chorusWrapper("\\mystrut " + lyrics)
        # else:
        songStr += lyrics
        songStr += "\\vspace{\\baselineskip}\n"
        songStr += "\\end{leftcolumn*}\n"
        if chords:
            songStr += "\\begin{rightcolumn}"
            songStr += "\\noindent"
            songStr += "\\begin{bfseries}"
            songStr += "\\ttfamily\n"
            if section.chorus:
                songStr += "\\mystrut "
            songStr += self.superscriptSpecialChars(chords)
            songStr += "\\end{bfseries}\n"
            songStr += "\\vspace{\\baselineskip}\n"
            songStr += "\\end{rightcolumn}\n"
            songStr += "\n\\rmfamily\n"
        return songStr, vspace

    def chorusWrapper(self, text):
        wrapped_text = "\\begin{chorus}" + text + "\\end{chorus}"
        return wrapped_text

    def convertLineBreaks(self, text, chords=False):
        converted_text = ""
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line:
                if (not chords) and config.devSettings['drawLines']:
                    converted_text += "\\tikz[overlay]\\draw[red](0,0)--++(20,0);"
                else:
                    converted_text += " "
                converted_text += line
                if i < len(lines)-1:
                    converted_text += "\\\\\n"
            else:
                converted_text += " \\\\\n"
        return converted_text, len(lines)


def makeSongbookDict(songs):
    songbookDict = CategoryDict()
    for category in songs:
        for song in category:
            songbookDict[song.category].songs[song.title] = song
    return songbookDict


async def getCategoriesConfig(categoryDictFile, songbookDict):
    try:
        async with aiofiles.open(categoryDictFile, "rb") as configFile:
            cats_dict = json.loads(deUTF8(await configFile.read()))
    except FileNotFoundError:
        logger.warning("Category titles mapping file not found")
        cats_dict = {cat: cat for cat in sorted(
            songbookDict.keys(), key=plSortKey)}
    return cats_dict


async def processCategory(cat, songbookFile, ignoredSongs=None):
    logger.info(f"Writing category {cat.name} to {songbookFile.name} file")
    keys = cat.songs.keys()
    ignoredCount = 0
    for songKey in sorted(keys, key=plSortKey):
        song = cat.songs[songKey]
        if (cat.name, song.title) not in ignoredSongs:
            logger.debug(f"Writing song {song.title} to {songbookFile.name} file")
            await songbookFile.write(enUTF8(song.tex))
        else:
            ignoredCount += 1
    return len(keys) - ignoredCount


async def processSingleSong(song, songbookFile):
    logger.info(f"Writing song {song.title} to {songbookFile.name} file")
    await songbookFile.write(enUTF8(song.tex))
    return 1


def main():
    return asyncio.run(_asyncMain())


async def _asyncMain():
    config.update()

    texOutFile = f"{config.outputFile}.tex"

    logger.debug(f"Copying header to {texOutFile}...")

    async with aiofiles.open(texOutFile, "wb") as songbookFile:
        await songbookFile.write(enUTF8(headerconfig.getHeader()))

    logger.info(f"Header copied")

    max_open_files = 100
    sem = asyncio.Semaphore(max_open_files)

    gatheredSongs = await gatherAllCategories(sem)

    songbookDict = makeSongbookDict(gatheredSongs)

    cats = await getCategoriesConfig(os.path.join(config.dataFolder, config.categoriesFile), songbookDict)

    for cat in songbookDict.values():
        cat.setCatMapping(cats)

    songCount = 0

    async with aiofiles.open(texOutFile, "ab") as songbookFile:

        titleSongs = [("Turystyczne", "Hawiarska Koliba")]
        for titleSong in titleSongs:
            try:
                songCount += await processSingleSong(songbookDict[titleSong[0]].songs[titleSong[1]], songbookFile)
            except KeyError:
                logger.warning(f"Title song {titleSong[0]} not found")
        await songbookFile.write(enUTF8("\n\t\\chapter*{Spis treści}\n\\begin{multicols}{2}\n\\tableofcontents\n\\end{multicols}\n"))

        for cat in cats.keys():
            if cat != "Title":
                await songbookFile.write(enUTF8(songbookDict[cat].tex))
                songCount += await processCategory(songbookDict[cat], songbookFile, titleSongs)

        await songbookFile.write(enUTF8(f"\\IfFileExists{{{config.outputFile}_list.toc}}{{\n\t\\chapter*{{Spis treści}}\n\\begin{{multicols}}{{2}}\n\t\\input{{{config.outputFile}_list.toc}}\n\\end{{multicols}}\n}}{{}}\n"))
        await songbookFile.write(enUTF8("\\end{document}"))
    logger.info(f"Total number of songs: {songCount}")
    return texOutFile

if __name__ == "__main__":
    main()
