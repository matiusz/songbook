import json, os
from collections import defaultdict
from src.tools.ResourcePath import resource_path

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
        self._configFilename = configFilename
        try:
            with open(self._configFilename, "rb") as configFile:
                config = json.loads(deUTF8(configFile.read()))
        except FileNotFoundError:
            config = json.loads(self.getDefaultConfig())
            print("WARN: Config file not found, using default config")
        self.loadFromDict(config)

    def loadFromDict(self, config):
        filePathConfig = config['filePaths']
        
        try:
            self.dataFolder = os.environ['SONGBOOK_DATA_DIR']
        except KeyError:
            self.dataFolder = 'data'
        self.categoriesFile = filePathConfig['categoriesFile']
        self.imageFolder = filePathConfig['imageFolder']
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
        #Date is currently generated automatically by headerconfig.py script
        #self.date = titlePageSettings['date']
        self.author = titlePageSettings['author']
        self.devSettings = defaultdict(lambda: False)
        try:
            for k, v in  config['devSettings'].items():
                self.devSettings[k] = v
        except KeyError:
            pass

    def update(self):
        try:
            with open(self._configFilename, "r") as configFile:
                config = json.load(configFile)
        except (FileNotFoundError, KeyError):
            print("WARN: Failed to parse new config file, config not updated.")
            return
        else:
            self.loadFromDict(config)

    def getDefaultConfig(self):
        return """{ 
            "filePaths": 
                {
                    "categoriesFile": "categories.json",
                    "imageFolder": ".images",
                    "outputFile": "songbook",
                    "appLogo": "logo.png"
                },
            "pdfSettings": 
            {
                "globalBold" : false,
                "chordShift": 0,
                "format": "a4paper",
                "sides": "oneside",
                "margins":
                {
                    "horizontal": 20,
                    "vertical": 15
                },
                "fontSize" : 12,
                "lyricsFont" : "ptm",
                "chordsFont" : "zi4",
                "titlePage" : {
                    "title" : "Śpiewnik Hawiarskiej Koliby\\\\Edycja Rozszerzona",
                    "author" : ""
                }
            },
            "devSettings":
            {
                "drawLines" : false,
                "singleCompile" : false,
                "keepAuxOut" : false
            }
        }"""


config = Configuration("config.json")

