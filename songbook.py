import os
import json
from collections import defaultdict

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
    songStr = "\\begin{paracol}{2}\n"
    text = convert_line_breaks(section['lyrics'])
    if section['chorus']:
        text = chorus_wrapper(text)
    songStr += text
    songStr += "\n\\switchcolumn\n\\ttfamily\n"
    songStr += convert_line_breaks(section['chords'])
    songStr += "\n\\rmfamily\n\\end{paracol}\n"
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


def main():
    configFilename = "categories.cfg"
    headerFilename = "latexheader.txt"
    headerFile = open(headerFilename, "rb")
    songbookFilename = "songbook.tex"
    if os.path.exists(songbookFilename):
        os.remove(songbookFilename)
    songbookFile = open(songbookFilename, "ab")
    songbookFile.write(headerFile.read())
    headerFile.close()
    
    categories = defaultdict(lambda: {})

    for dirname in os.listdir():
        if os.path.isdir(dirname) and not dirname.startswith("."):
            for filename in os.listdir(dirname):
                if filename.endswith(".sng"):
                    songFile = open(os.path.join(dirname, filename))
                    song = json.loads(songFile.read())
                    categories[song['category']][song['title']] = song

    if os.path.exists("categories.cfg"):
        configFile = open("categories.cfg", "rb")
        cats_text = de_utf8(configFile.read())
        cats = cats_text.splitlines()

    cats = [cat for cat in cats if cat and not cat.startswith("#")]

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
