import dirTools

import os

def loadSongs():
    cats = dirTools.getCategoriesFromDirs()
    songFilenames = []
    for cat in cats:
        songFilenames.extend([os.path.join(os.getcwd(), "data", cat, song)for song in dirTools.getSongsFromCatDir(cat)])
    return songFilenames

def replaceInFile(fileName, pairs):
    try:
        with open(fileName, "r+") as text_file:
            texts = text_file.read()
            for p in pairs:
                if texts.find(p[0])!=-1:
                    print(fileName)
                texts = texts.replace(p[0], p[1])
        with open(fileName, "w") as text_file:
            text_file.write(texts)
    except FileNotFoundError as f:
        print("Could not find the file you are trying to read.")

songFilenames = loadSongs()
pairs = [("    \"", "****\""), (": \"", ":::\""), ("\\n ","\\n"), (" \\n","\\n"), ("\" ","\""), (" \"","\""), (":::\"",": \""), ("****\"", "    \""), ("\\n\"", "\"")]
[replaceInFile(songFilename, pairs) for songFilename in songFilenames]