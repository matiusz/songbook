import json
import os

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

config = Configuration("fileConfig.json")


