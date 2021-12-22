import json
from collections import defaultdict


def enUTF8(st):
    return st.encode('utf-8')
def deUTF8(st):
    return st.decode('utf-8')

class Margins:
    def __init__(self, vertical, horizontal):
        self.vertical = vertical
        self.horizontal = horizontal

class Canvas:
    def __init__(self, format, sides, margins):
        self.format = format
        self.sides = sides
        self.margins = Margins(margins['vertical'], margins['horizontal'])

class Configuration:
    def __init__(self, configFilename):
        with open(configFilename, "rb") as configFile:
            config = json.loads(deUTF8(configFile.read()))

        filePathConfig = config['filePaths']
        
        self.dataFolder = filePathConfig['dataFolder']
        self.categoriesFile = filePathConfig['categoriesFile']
        self.imageFolder = filePathConfig['imageFolder']
        self.latexHeaderFile = filePathConfig['latexHeaderFile']
        self.outputFile = filePathConfig['outputFile']
        self.appLogo = filePathConfig['appLogo']

        pdfSettings = config['pdfSettings']

        self.chordShift = pdfSettings['chordShift']

        self.globalBold = pdfSettings['globalBold']

        self.canvas = Canvas(pdfSettings['format'], pdfSettings['sides'], pdfSettings['margins'])

        self.fontSize = pdfSettings['fontSize']
        
        self.lyricsFont = pdfSettings['lyricsFont']

        self.chordsFont = pdfSettings['chordsFont']

        titlePageSettings = pdfSettings['titlePage']

        self.title = titlePageSettings['title']

        #self.date = titlePageSettings['date']

        self.author = titlePageSettings['author']

        try:
            self.devSettings = config['devSettings']
        except KeyError:
            self.devSettings = defaultdict(lambda: False)


config = Configuration("config.json")


