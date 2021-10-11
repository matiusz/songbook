import json
import os

class Configuration:
    def __init__(self, configFile):
        with open(configFile, "r") as configFile:
            config = json.load(configFile)
        self.dataFolder = config['dataFolder']
        self.categoriesFile = config['categoriesFile']
        self.imageFolder = config['imageFolder']
        self.latexHeaderFile = config['latexHeaderFile']
        self.outputFile = config['outputFile']
        self.appLogo = config['appLogo']

config = Configuration("fileConfig.json")


