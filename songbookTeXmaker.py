import os
import json
from collections import defaultdict
import re
from plAlphabetSort import plSortKey
import asyncio
import aiofiles

from chordShift import shiftChords

def enUTF8(st):
    return st.encode('utf-8')
def deUTF8(st):
    return st.decode('utf-8')

async def gatherCategories(dataFolder):
    tasks = [gatherSongs(dirpath) for dirname in os.listdir(dataFolder) \
        if os.path.isdir(dirpath := os.path.join(dataFolder, dirname)) and not (dirname.startswith((".", "_")))]
    categories = await asyncio.gather(*tasks)
    return categories

async def gatherSongs(dirpath):
    tasks = [Song.load(dirpath, filename) for filename in os.listdir(dirpath) if filename.endswith(".sng")]
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
    def tex(self):
        catStr = "\\chapter*{{\centering {category}}}\n".format(category=self.name) + \
        "\\addcontentsline{{toc}}{{chapter}}{{{category}}}\n".format(category=self.name) + \
        "{{\\centering \\includegraphics[width=\\textwidth,height=0.75\\textheight,keepaspectratio]{{{category}}} \\par}}\n".format(category=self.name) + \
        "\\newpage\n"
        #catStr += "\\cleardoublepage\n"
        return catStr

class Song:
    @staticmethod
    async def load(dirpath, filename):
        async with aiofiles.open(os.path.join(dirpath, filename), "r") as songFile:
            song = Song(await songFile.read())
        return song

    def __init__(self, file):
        self.dict = json.loads(file)
        self.title = self.dict['title']
        self.category = self.dict['category']
    def tex(self):
        songStr = "\\section*{{{title}}}\n\\addcontentsline{{toc}}{{section}}{{{title}}}\n\\columnratio{{0.8,0.2}}\n".format(title=self.title)
        try:
            author = self.dict['author']
        except KeyError:
            pass
        else:
            songStr += "\\begin{{flushright}}\n{author}\n\\end{{flushright}}".format(author = author)
        try:
            capo = self.dict['capo']
        except KeyError:
            pass
        else:
            songStr += "\\begin{{flushright}}\n{capo}\n\\end{{flushright}}".format(capo = capo)     
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
        wrapped_text = "\\begin{chorus}\n"
        wrapped_text += text
        wrapped_text += "\\end{chorus}\n"
        return wrapped_text

    def convertLineBreaks(self, text):
        converted_text = ""
        length = 0
        for line in text.splitlines():
            if line:
                converted_text += line + "\\\\\n" 
            else:
                converted_text += "\\vspace{\\baselineskip}\n"
            length +=1
        return converted_text, length

def main():
    asyncio.run(asyncMain())

async def asyncMain():
    configFilename = "categories.cfg"
    headerFilename = "latexheader.txt"
    songbookFilename = "songbook.tex"
    dataFolder = "data"
    async with aiofiles.open(songbookFilename, "wb") as songbookFile:
        async with aiofiles.open(headerFilename, "rb") as headerFile:
            await songbookFile.write(await headerFile.read())
    
        songbookDict = CategoryDict()

        gatheredSongs = await gatherCategories(dataFolder)

        for category in gatheredSongs:
            for song in category:
                songbookDict[song.category].songs[song.title] = song

        try:
            async with aiofiles.open(os.path.join(dataFolder, configFilename), "rb") as configFile:
                cats_text = deUTF8(await configFile.read())
        except FileNotFoundError:
            cats = sorted(songbookDict.keys(), key=plSortKey)
        else:
            cats = [cat for cat in cats_text.splitlines() if not cat.startswith("#")]
        songCount = 0
        print("Title songs")
        for song in songbookDict["Title"].songs.values():
            songCount += 1
            print("\t" + song.title)
            await songbookFile.write(enUTF8(song.tex()))
        await songbookFile.write(enUTF8("\\tableofcontents\n"))
        for cat in cats:
            if cat != "Title":
                print(cat)
                await songbookFile.write(enUTF8(songbookDict[cat].tex()))
                for song in sorted(songbookDict[cat].songs.keys(), key=plSortKey):
                    songCount += 1
                    print("\t" + song)
                    await songbookFile.write(enUTF8(songbookDict[cat].songs[song].tex()))
        await songbookFile.write(enUTF8("\\IfFileExists{songlist.toc}{\n\t\\chapter*{Spis treści}\n\t\\input{songlist.toc}\n}{}\n"))
        await songbookFile.write(enUTF8("\\end{document}"))
        print("Total number of songs: {songCount}".format(songCount=songCount))
    
if __name__=="__main__":
    main()
