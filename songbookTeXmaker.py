import os
import json
from collections import defaultdict
import re
from plAlphabetSort import plSortKey

from chordShift import chordShift, shiftChords

def enUTF8(st):
    return st.encode('utf-8')
def deUTF8(st):
    return st.decode('utf-8')

def songToTex(songJSON):
    songStr = "\\section*{{{title}}}\n\\addcontentsline{{toc}}{{section}}{{{title}}}\n\\columnratio{{0.8,0.2}}\n".format(title=songJSON['title'])
    try:
        author = songJSON['author']
    except KeyError:
        pass
    else:
        songStr += "\\begin{{flushright}}\n{author}\n\\end{{flushright}}".format(author = author)
    try:
        capo = songJSON['capo']
    except KeyError:
        pass
    else:
        songStr += "\\begin{{flushright}}\n{capo}\n\\end{{flushright}}".format(capo = capo)     
    songStr += "\\begin{paracol}{2}\n"
    for section in songJSON['sections']:
        songStr += convertSection(section)
    songStr += "\\end{paracol}\n"
    songStr += "\\newpage\n"
    return songStr


def superscriptSpecialChars(text):
    specialChars = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "*", "sus", "add", "/"]
    chDict = {}
    for idx, ch in enumerate(specialChars):
        chDict[ch] = ("\\textsuperscript{{{char}}}".format(char = ch))
    pattern = re.compile('|'.join(sorted([re.escape(key) for key in chDict.keys()], key=len, reverse=True)))
    result = pattern.sub(lambda x: chDict[x.group()], text)
    return result

def convertSection(section):
    chordShift = 0
    lyrics, l1 = convertLineBreaks(section['lyrics'])
    if section['chords']:
        chords, l2 = convertLineBreaks(shiftChords(section['chords'], chordShift).replace("\\", "\\textbackslash "))
    else:
        chords, l2 = "", 0
    songStr = "\n\\ensurevspace{{{linecount}\\baselineskip}}\n".format(linecount = max(l1, l2))
    songStr += "\\begin{leftcolumn*}\n"
    if section['chorus']:
        lyrics = chorusWrapper(lyrics)
    songStr += lyrics
    songStr += "\\end{leftcolumn*}\n"
    if chords:
        songStr += "\\begin{rightcolumn}\n"
        songStr += "\\begin{bfseries}\n"
        songStr += "\n\\ttfamily\n"
        songStr += superscriptSpecialChars(chords)
        songStr += "\\end{bfseries}\n"
        songStr += "\\end{rightcolumn}\n"
        songStr += "\n\\rmfamily\n"
    return songStr

def chorusWrapper(text):
    wrapped_text = "\\begin{chorus}\n"
    wrapped_text += text
    wrapped_text += "\\end{chorus}\n"
    return wrapped_text

def convertLineBreaks(text):
    converted_text = ""
    length = 0
    for line in text.splitlines():
        if line:
            converted_text += line + "\\\\\n" 
        else:
            converted_text += "\\vspace{\\baselineskip}\n"
        length +=1
    return converted_text, length

def categoryToTex(category):
    catStr = "\\chapter*{{\centering {category}}}\n".format(category=category) + \
        "\\addcontentsline{{toc}}{{chapter}}{{{category}}}\n".format(category=category) + \
        "{{\\centering \\includegraphics[width=\\textwidth,height=0.75\\textheight,keepaspectratio]{{{category}}} \\par}}\n".format(category=category) + \
        "\\newpage\n"
    #catStr += "\\cleardoublepage\n"
    return catStr


def main():
    configFilename = "categories.cfg"
    headerFilename = "latexheader.txt"
    dataFolder = "data"
    headerFile = open(headerFilename, "rb")
    songbookFilename = "songbook.tex"
    songbookFile = open(songbookFilename, "wb")
    songbookFile.write(headerFile.read())
    headerFile.close()
    
    categories = defaultdict(lambda: {})

    for dirname in os.listdir(dataFolder):
        if os.path.isdir(dirpath := os.path.join(dataFolder, dirname)) and not (dirname.startswith((".", "_"))):
            for filename in os.listdir(dirpath):
                if filename.endswith(".sng"):
                    songFile = open(os.path.join(dirpath, filename))
                    song = json.loads(songFile.read())
                    categories[song['category']][song['title']] = song
    try:
        with open(os.path.join(dataFolder, configFilename), "rb") as configFile:
            cats_text = deUTF8(configFile.read())
    except FileNotFoundError:
        cats = sorted(categories.keys(), key=plSortKey)
    else:
        cats = [cat for cat in cats_text.splitlines() if not cat.startswith("#")]
    songCount = 0
    for cat in cats:
        print(cat)
        songbookFile.write(enUTF8(categoryToTex(cat)))
        for song in sorted(categories[cat].keys(), key=plSortKey):
            songCount += 1
            print("\t" + song)
            songbookFile.write(enUTF8(songToTex(categories[cat][song])))
    songbookFile.write(enUTF8("\\IfFileExists{songlist.toc}{\n\t\\chapter*{Spis treści}\n\t\\input{songlist.toc}\n}{}\n"))
    songbookFile.write(enUTF8("\\end{document}"))
    songbookFile.close()
    print("Total number of songs: {songCount}".format(songCount=songCount))

if __name__=="__main__":
    main()
