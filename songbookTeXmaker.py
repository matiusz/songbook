import os
import json
import re
from plAlphabetSort import plSortKey
import asyncio
import aiofiles

from chordShift import shiftChords

def enUTF8(st):
    return st.encode('utf-8')
def deUTF8(st):
    return st.decode('utf-8')

async def gatherAllCategories(dataFolderName):
    tasks = [gatherSongs(dirpath) for dirname in os.listdir(dataFolderName) \
        if os.path.isdir(dirpath := os.path.join(dataFolderName, dirname)) and not (dirname.startswith((".", "_")))]
    categories = await asyncio.gather(*tasks)
    return categories

async def gatherSongs(dirpath):
    tasks = [Song.load(os.path.join(dirpath, filename)) for filename in os.listdir(dirpath) if filename.endswith(".sng")]
    songs = await asyncio.gather(*tasks)
    return songs
    

class CategoryDict(dict):
    def __missing__(self, key):
        res = self[key] = Category(key)
        return res

class Category:
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
        catStr = "\\chapter*{{\centering {category}}}\n".format(category=name) + \
        "\\addcontentsline{{toc}}{{chapter}}{{{category}}}\n".format(category=name) + \
        "{{\\centering \\includegraphics[width=\\textwidth,height=0.75\\textheight,keepaspectratio]{{{category}}} \\par}}\n".format(category=self.name) + \
        "\\newpage\n"
        #catStr += "\\cleardoublepage\n"
        return catStr

class Song:
    @staticmethod
    async def load(filepath):
        async with aiofiles.open(filepath, "r") as songFile:
            song = Song(await songFile.read())
        return song

    def __init__(self, songJSON):
        self.dict = json.loads(songJSON)
        self.title = self.dict['title']
        self.category = self.dict['category']
    @property
    def tex(self):
        songStr = "\\section*{{{title}}}\n\\addcontentsline{{toc}}{{section}}{{{title}}}\n\\columnratio{{0.8,0.2}}\n\\rmfamily".format(title=self.title)
        try:
            author = self.dict['author']
            songStr += "\\begin{{flushright}}\n{author}\n\\end{{flushright}}".format(author = author)
        except KeyError:
            pass
        try:
            capo = self.dict['capo']
            songStr += "\\begin{{flushright}}\n{capo}\n\\end{{flushright}}".format(capo = capo)     
        except KeyError:
            pass
        songStr += "\\begin{paracol}{2}\n"
        for section in self.dict['sections']:
            songStr += self.convertSection(section)
        songStr += "\\end{paracol}\n"
        songStr += "\\newpage\n"
        return songStr

    def superscriptSpecialChars(self, text):
        specialChars = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "*", "sus", "add", "/"]
        chDict = {}
        for ch in specialChars:
            chDict[ch] = ("\\textsuperscript{{{char}}}".format(char = ch))
        pattern = re.compile('|'.join(sorted([re.escape(key) for key in chDict.keys()], key=len, reverse=True)))
        result = pattern.sub(lambda x: chDict[x.group()], text)
        return result
        
    def convertSection(self, section):
        chordShift = 0
        lyrics, l1 = self.convertLineBreaks(section['lyrics'])
        if section['chords']:
            chords, l2 = self.convertLineBreaks(shiftChords(section['chords'], chordShift).replace("\\", "\\textbackslash "))
        else:
            chords, l2 = "", 0
        songStr = "\n\\ensurevspace{{{linecount}\\baselineskip}}\n".format(linecount = max(l1, l2))
        songStr += "\\begin{leftcolumn*}\n"
        if section['chorus']:
            lyrics = self.chorusWrapper(lyrics)
        songStr += lyrics
        songStr += "\\end{leftcolumn*}\n"
        if chords:
            songStr += "\\begin{rightcolumn}\n"
            songStr += "\\begin{bfseries}\n"
            songStr += "\n\\ttfamily\n"
            songStr += self.superscriptSpecialChars(chords)
            songStr += "\\end{bfseries}\n"
            songStr += "\\end{rightcolumn}\n"
            songStr += "\n\\rmfamily\n"
        return songStr

    def chorusWrapper(self, text):
        wrapped_text = "\\begin{chorus}\n" + text + "\\end{chorus}\n"
        return wrapped_text

    def convertLineBreaks(self, text):
        converted_text = ""
        lines = text.splitlines()
        for line in lines:
            if line:
                converted_text += line + "\\\\\n" 
            else:
                converted_text += "\\vspace{\\baselineskip}\n"
        return converted_text, len(lines)

async def copyHeader(headerFilename, songbookFilename):
    async with aiofiles.open(songbookFilename, "wb") as songbookFile:
        async with aiofiles.open(headerFilename, "rb") as headerFile:
            await songbookFile.write(await headerFile.read())

def makeSongbookDict(songs):
    songbookDict = CategoryDict()
    for category in songs:
        for song in category:
            songbookDict[song.category].songs[song.title] = song
    return songbookDict

async def getCategoriesConfig(configFilepath, songbookDict):
    try:
        async with aiofiles.open(configFilepath, "rb") as configFile:
            cats_dict = json.loads(deUTF8(await configFile.read()))
    except FileNotFoundError:
        print("mapping not found")
        cats_dict = {cat:cat for cat in sorted(songbookDict.keys(), key=plSortKey)}
    return cats_dict

async def processCategoryFromDict(cat, songbookFile):
    keys = cat.songs.keys()
    for songKey in sorted(keys, key=plSortKey):
        song = cat.songs[songKey]
        print("\t" + song.title)
        await songbookFile.write(enUTF8(song.tex))
    return len(keys)

def main():
    asyncio.run(_asyncMain())

async def _asyncMain():
    configFilename = "categories.cfg"
    headerFilename = "latexheader.txt"
    songbookFilename = "songbook.tex"
    dataFolderName = "data"
    
    await copyHeader(headerFilename, songbookFilename)
    
    gatheredSongs = await gatherAllCategories(dataFolderName)

    songbookDict = makeSongbookDict(gatheredSongs)

    cats = await getCategoriesConfig(os.path.join(dataFolderName, configFilename), songbookDict)

    for cat in songbookDict.values():
        cat.setCatMapping(cats)

    songCount = 0
    print("Title songs")

    async with aiofiles.open(songbookFilename, "ab") as songbookFile:

        songCount += await processCategoryFromDict(songbookDict["Title"], songbookFile)
        
        await songbookFile.write(enUTF8("\\tableofcontents\n"))

        for cat in cats.keys():
            if cat != "Title":
                print(cat)
                await songbookFile.write(enUTF8(songbookDict[cat].tex))
                songCount += await processCategoryFromDict(songbookDict[cat], songbookFile)

        await songbookFile.write(enUTF8("\\IfFileExists{songlist.toc}{\n\t\\chapter*{Spis treści}\n\t\\input{songlist.toc}\n}{}\n"))
        await songbookFile.write(enUTF8("\\end{document}"))
    print("Total number of songs: {songCount}".format(songCount=songCount))
    
if __name__=="__main__":
    main()
