from src.obj.Config import config
import os

def docClass(form, sides, size):
    return f"\\documentclass[{form}, {sides}, {size}pt]{{report}}\n"
    
def packages(packs):
    string = ""
    for pack in packs:
        if isinstance(pack, tuple):
            string += f"\\usepackage[{pack[1]}]{{{pack[0]}}}\n"
        else:
            string += f"\\usepackage{{{pack}}}\n"
    string += "\n"
    return string

def getPackageList():
    return [("fontenc", "T1"), ("babel", "english"), "blindtext", "paracol", "geometry", "indentfirst", "changepage", "graphicx", "hyperref"]

def hyperSetup():
    return "\\hypersetup{\n    hidelinks,\n    linktoc=all\n}\n\n"

def minorSettings():
    return "\\graphicspath{{./data/.images/}}\n\\setlength\\parindent{0pt}\n\n\\hbadness=15000  % or any number >=10000" + \
    "\n\\vfuzz = 15pt\n\n% HACKING \\adjustwidth\n\\usepackage{etoolbox}\n\\makeatletter\n\\apptocmd\\adjustwidth{\@inlabelfalse\@newlistfalse}\n\\makeatother\n\n"

def geometry(form, width, height, horizontal, vertical, sides):
    return f"\\geometry{{\n {form},\n total={{{width}mm,{height}mm}},\n {'inner' if sides == 'twoside' else 'left'}={horizontal}mm,\n top={vertical}mm,\n }}\n\n"

def minorSettings2():
    return "\\begin{document}\n\n" + makeTitle() +"\\newenvironment{chorus}{\\begin{adjustwidth}{2cm}{}}{\\end{adjustwidth}}\n\n"
    
def font():
    return f"\\renewcommand{{\\rmdefault}}{{{config.lyricsFont}}}\n\\renewcommand{{\\ttdefault}}{{{config.chordsFont}}}\n\n"

def toc():
    return "\\renewcommand{\\contentsname}{Spis treści}\n"

def titleSettings():
    return f"\\title{{{config.title}}}\n\\date{{{config.date}}}\n\\author{{{config.author}}}\n\n"

def makeTitle():
    return "\\begin{titlepage}\n\\maketitle\n\\end{titlepage}\n\n"


def assembleHeader():
    header = ""
    form = config.canvas.format
    sides = config.canvas.sides
    vertical = config.canvas.margins.vertical
    horizontal = config.canvas.margins.horizontal
    width = config.canvas.textFieldSize.width
    height = config.canvas.textFieldSize.height
    
    header += docClass(form = form, sides = sides, size = config.fontSize)
    header += packages(getPackageList())
    header += hyperSetup()
    header += minorSettings()
    header += geometry(form = form, width = width, height = height, horizontal = horizontal, vertical = vertical, sides = sides)
    header += titleSettings()
    header += minorSettings2()
    header += font()
    header += toc()
    return header

def main():
    with open(os.path.join(config.dataFolder, config.latexHeaderFile), "wb") as headerFile:
        headerFile.write(assembleHeader().encode("utf-8"))


if __name__=="__main__":
    main()