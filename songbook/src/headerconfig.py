from .obj.Config import config
import os
from datetime import date

months = [
    "Styczeń",
    "Luty",
    "Marzec",
    "Kwiecień",
    "Maj",
    "Czerwiec",
    "Lipiec",
    "Sierpień",
    "Wrzesień",
    "Październik",
    "Listopad",
    "Grudzień",
]


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
    return [
        ("fontenc", "T1"),
        ("babel", "english"),
        "blindtext",
        "paracol",
        "geometry",
        "indentfirst",
        "changepage",
        "graphicx",
        "hyperref",
        "multicol",
        "tikz",
        "zi4",
    ]


def hyperSetup():
    return "\\hypersetup{\n    hidelinks,\n    linktoc=all\n}\n\n"


def minorSettings():
    imgPath = (
        os.path.join(config.dataFolder, config.imageFolder)
        .replace("\\", "//", 1)
        .replace("\\", "/")
        + "/"
    )
    return (
rf"""\graphicspath{{{{{imgPath}}}}}
\setlength\parindent{{0pt}}

\hbadness=15000  % or any number >=10000
\vfuzz = 15pt

% HACKING \adjustwidth
\usepackage{{etoolbox}}
\makeatletter
\apptocmd\adjustwidth{{\@inlabelfalse\@newlistfalse}}
\makeatother
\raggedbottom
"""
    )


def geometry(form, horizontal, vertical, sides):
    return f"\\geometry{{\n {form},\n {'inner' if sides == 'twoside' else 'left'}={horizontal}mm,\n top={vertical}mm,\n {'outer' if sides == 'twoside' else 'right'}=15mm, \n  bottom={vertical}mm, \n}}\n\n"


def beginDoc():
    string = f"\\newcommand\\mystrut{{\\rule{{0pt}}{{{config.fontSize}pt}}}}\n"
    if config.globalBold:
        string += "\\renewcommand{\\seriesdefault}{\\bfdefault}\n\n"
    string += "\\begin{document}\n\n"
    return string


def minorSettings2():
    return (
        "\\newenvironment{chorus}{\\begin{adjustwidth}{2cm}{}}{\\end{adjustwidth}}\n\n"
    )


def font():
    return f"\\renewcommand{{\\rmdefault}}{{{config.lyricsFont}}}\n\\renewcommand{{\\ttdefault}}{{{config.chordsFont}}}\n\n"


def toc():
    # hack avoiding insertion of the toc header, which doesn't play well with 2 columns
    return "\\renewcommand{\\contentsname}{\\vspace*{-104pt}}\n"


def titleSettings():
    onePercentHack = (
        r"""\vspace{0.40\textheight} \\1 \% podatku dla “Hawiarskiej Koliby”\\
        Numer KRS 0000083727\\
        Z dopiskiem:\\
        Cel szczegółowy: Koło nr 2 Hawiarska Koliba\\
        Dziękujemy!"""
    )
    today = date.today()
    return f"\\title{{{config.title}}}\n\\date{{{months[today.month-1]} {today.year}}}\n\\author{{{onePercentHack}}}\n\n"


def makeTitle():
    return "\\begin{titlepage}\n\\maketitle\n\\end{titlepage}\n\n"


def getHeader():
    header = ""
    form = config.canvas.format
    sides = config.canvas.sides
    vertical = config.canvas.margins.vertical
    horizontal = config.canvas.margins.horizontal

    header += docClass(form=form, sides=sides, size=config.fontSize)
    header += packages(getPackageList())
    header += hyperSetup()
    header += minorSettings()
    header += geometry(form=form, horizontal=horizontal, vertical=vertical, sides=sides)
    header += titleSettings()
    header += beginDoc()
    header += makeTitle()
    header += minorSettings2()
    header += font()
    header += toc()
    return header
