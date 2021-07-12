import os
import json
from collections import defaultdict
import math

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
        
    songStr += "\\begin{paracol}{2}\n"
    for section in songJSON['sections']:
        songStr += convertSection(section)
    songStr += "\\end{paracol}\n"
    songStr += "\\newpage\n"
    return songStr

def convertSection(section):
    lyrics, l1 = convertLineBreaks(section['lyrics'])
    if section['chords']:
        chords, l2 = convertLineBreaks(section['chords'])
    else:
        chords, l2 = "", 0
    songStr = "\n\\ensurevspace{{{}\\baselineskip}}\n".format(max(l1, l2))
    songStr += "\\begin{leftcolumn*}\n"
    if section['chorus']:
        lyrics = chorusWrapper(lyrics)
    songStr += lyrics
    songStr += "\\end{leftcolumn*}\n"
    if chords:
        songStr += "\\begin{rightcolumn}\n"
        
        songStr += "\n\\ttfamily\n"
        songStr += chords
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
        "\\includegraphics[width=\\textwidth]{{{category}}}\n".format(category=category) + \
        "\\newpage\n"
    return catStr


def main():
    configFilename = "categories.cfg"
    headerFilename = "latexheader.txt"
    dataFolder = "data"
    headerFile = open(headerFilename, "rb")
    songbookFilename = "songbook.tex"
    if os.path.exists(songbookFilename):
        os.remove(songbookFilename)
    songbookFile = open(songbookFilename, "ab")
    songbookFile.write(headerFile.read())
    headerFile.close()
    
    categories = defaultdict(lambda: {})

    for dirname in os.listdir(dataFolder):
        if os.path.isdir(os.path.join(dataFolder, dirname)) and not (dirname.startswith(".") or dirname.startswith("_")):
            for filename in os.listdir(os.path.join(dataFolder, dirname)):
                if filename.endswith(".sng"):
                    songFile = open(os.path.join(dataFolder, dirname, filename))
                    song = json.loads(songFile.read())
                    categories[song['category']][song['title']] = song

    cats = []
    if os.path.exists(os.path.join(dataFolder, configFilename)):
        configFile = open(os.path.join(dataFolder, configFilename), "rb")
        cats_text = deUTF8(configFile.read())
        cats = [cat for cat in cats_text.splitlines() if not cat.startswith("#")]

    cats = cats or sorted(categories.keys())
    
    for cat in cats:
        print(cat)
        songbookFile.write(enUTF8(categoryToTex(cat)))
        for song in sorted(categories[cat].keys()):
            print("\t" + song)
            songbookFile.write(enUTF8(songToTex(categories[cat][song])))
    songbookFile.write(enUTF8("\\IfFileExists{songlist.toc}{\input{songlist.toc}}{}\n"))
    songbookFile.write(enUTF8("\\end{document}"))
    songbookFile.close()

if __name__=="__main__":
    main()
