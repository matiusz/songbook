import os
import json
from collections import defaultdict

def songToTex(songJSON):
    songStr = "\\section*{{{title}}}\n\\addcontentsline{{toc}}{{section}}{{{title}}}\n\\columnratio{{0.7,0.3}}\n".format(title=songJSON['title'])
    for section in songJSON['sections']:
        songStr += convert_section(section)
    songStr += "\\newpage\n"
    return songStr

def convert_section(section):
    songStr = "\\begin{paracol}{2}\n"
    text = convert_line_breaks(section['lyrics'])
    if section['chorus']:
        text = chorus_wrapper(text)
    songStr += text
    songStr += "\n\\switchcolumn\n"
    songStr += convert_line_breaks(section['chords'])
    songStr += "\n\\end{paracol}\n"
    return songStr

def chorus_wrapper(text):
    wrapped_text = "\\begin{chorus}\n"
    wrapped_text += text
    wrapped_text += "\\end{chorus}\n"
    return wrapped_text

def convert_line_breaks(text):
    converted_text = ""
    for line in text.splitlines():
        if line:
            converted_text += line + "\\\\\n" 
        else:
            converted_text += "\\vspace{\\baselineskip}\n"
    return converted_text

def categoryToTex(category):
    catStr = "\\chapter*{{\centering {category}}}\n".format(category=category) + \
        "\\addcontentsline{{toc}}{{chapter}}{{{category}}}\n".format(category=category) + \
        "\\includegraphics[width=\\textwidth]{{{category}}}\n".format(category=category) + \
        "\\newpage\n"
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
            for filename in os.listdir(dirname):
                if filename.endswith(".sng"):
                    songfile = open(os.path.join(dirname, filename))
                    song = json.loads(songfile.read())
                    categories[song['category']][song['title']] = song

    if os.path.exists("categories.cfg"):
        f = open("categories.cfg", "rb")
        cats_text = f.read().decode("utf-8")
        cats = cats_text.splitlines()

    cats = cats or categories.keys()
    
    for cat in cats:
        print(cat)
        songbookFile.write(categoryToTex(cat).encode('utf-8'))
        for song in sorted(categories[cat].keys()):
            print("\t" + song)
            songbookFile.write(songToTex(categories[cat][song]).encode('utf-8'))
    songbookFile.write("\end{document}".encode('utf-8'))
    songbookFile.close()
