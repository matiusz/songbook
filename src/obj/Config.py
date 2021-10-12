import json
from src.tools.ResourcePath import resource_path


class TextField:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Margins:
    def __init__(self, vertical, horizontal):
        self.vertical = vertical
        self.horizontal = horizontal

class Canvas:
    def __init__(self, format, sides, textFieldSize, margins):
        self.format = format
        self.sides = sides
        self.textFieldSize = TextField(textFieldSize['width'], textFieldSize['height'])
        self.margins = Margins(margins['vertical'], margins['horizontal'])

class Configuration:
    def __init__(self, configFile):
        with open(configFile, "r") as configFile:
            config = json.load(configFile)

        filePathConfig = config['filePaths']
        
        self.dataFolder = filePathConfig['dataFolder']
        self.categoriesFile = filePathConfig['categoriesFile']
        self.imageFolder = filePathConfig['imageFolder']
        self.latexHeaderFile = filePathConfig['latexHeaderFile']
        self.outputFile = filePathConfig['outputFile']
        self.appLogo = filePathConfig['appLogo']

        baseSettings = config['baseSettings']

        self.chordShift = baseSettings['chordShift']

        self.canvas = Canvas(baseSettings['format'], baseSettings['sides'], baseSettings['textFieldSize'], baseSettings['margins'])

        self.fontSize = baseSettings['fontSize']
        
config = Configuration(resource_path("config.json"))


