import os
import json
from collections import defaultdict

def songToTex(songJSON):
    songStr = "\\section*{{{title}}}\n\\addcontentsline{{toc}}{{section}}{{{title}}}\n\\columnratio{{0.7,0.3}}\n".format(title=songJSON['title'])
    for section in songJSON['sections']:
        songStr += "\\begin{paracol}{2}\n"
        if section['chorus']:
            songStr += "\\begin{chorus}\n"
        for line in section['lyrics'].splitlines():
            if line:
                songStr += line + "\\\\\n" 
            else:
                songStr += "\\vspace{\\baselineskip}\n"
        if section['chorus']:
            songStr += "\\end{chorus}\n"
        songStr += "\n\\switchcolumn\n"
        for line in section['chords'].splitlines():
            if line:
                songStr += line + "\\\\\n" 
            else:
                songStr += "\\vspace{\\baselineskip}\n"
        songStr += "\n\\end{paracol}\n"
    songStr += "\\newpage\n"
    return songStr


def categoryToTex(category):
    catStr = "\\chapter*{{{category}}}\n".format(category=category) + \
    "\\addcontentsline{{toc}}{{chapter}}{{{category}}}\n".format(category=category)
    return catStr


if __name__=="__main__":
    headfileName = "latexheader.txt"
    headfile = open(headfileName, "rb")
    songbookFileName = "songbook.tex"
    if os.path.exists(songbookFileName):
        os.remove(songbookFileName)
    songbookFile = open(songbookFileName, "ab")
    songbookFile.write(headfile.read())
    categories = defaultdict(lambda: {})
    headfile.close()
    

    for dirname in os.listdir():
        if os.path.isdir(dirname) and not dirname.startswith("."):
            #songbookFile.write(categoryToTex(dirname).encode('utf-8'))
            for filename in os.listdir(dirname):
                if filename.endswith(".sng"):
                    songfile = open(os.path.join(dirname, filename))
                    song = json.loads(songfile.read())
                    categories[song['category']][song['title']] = song
    for cat in sorted(categories.keys()):
        print(cat)
        songbookFile.write(categoryToTex(cat).encode('utf-8'))
        for song in sorted(categories[cat].keys()):
            print("\t" + song)
            songbookFile.write(songToTex(categories[cat][song]).encode('utf-8'))
    songbookFile.write("\end{document}".encode('utf-8'))
    songbookFile.close()



