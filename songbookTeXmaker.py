import os
import json
from collections import defaultdict
import math

def en_utf8(st):
    return st.encode('utf-8')
def de_utf8(st):
    return st.decode('utf-8')

def songToTex(songJSON):
    songStr = "\\section*{{{title}}}\n\\addcontentsline{{toc}}{{section}}{{{title}}}\n\\columnratio{{0.7,0.3}}\n".format(title=songJSON['title'])
    for section in songJSON['sections']:
        songStr += convert_section(section)
    songStr += "\\newpage\n"
    return songStr

def convert_section(section):
    lyrics, l1 = convert_line_breaks(section['lyrics'])
    chords, l2 = convert_line_breaks(section['chords'])
    songStr = "\\begin{paracol}{2}\n"
    songStr += "\\ensurevspace{{{}\\baselineskip}}\n".format(max(l1, l2))
    songStr += "\\begin{leftcolumn*}\n"
    if section['chorus']:
        lyrics = chorus_wrapper(lyrics)
    songStr += lyrics
    songStr += "\n\\end{leftcolumn*}\n\\ttfamily\n"
    songStr += "\\begin{rightcolumn}\n"
    songStr += chords
    songStr += "\n\\rmfamily\n"
    songStr += "\\end{rightcolumn}\n"
    songStr += "\\end{paracol}\n"
    return songStr

def chorus_wrapper(text):
    wrapped_text = "\\begin{chorus}\n"
    wrapped_text += text
    wrapped_text += "\\end{chorus}\n"
    return wrapped_text

def convert_line_breaks(text):
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
        cats_text = de_utf8(configFile.read())
        cats = [cat for cat in cats_text.splitlines() if not cat.startswith("#")]

    cats = cats or sorted(categories.keys())
    
    for cat in cats:
        print(cat)
        songbookFile.write(en_utf8(categoryToTex(cat)))
        for song in sorted(categories[cat].keys()):
            print("\t" + song)
            songbookFile.write(en_utf8(songToTex(categories[cat][song])))
    songbookFile.write(en_utf8("\end{document}"))
    songbookFile.close()

if __name__=="__main__":
    main()
