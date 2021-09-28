import os

def ensureFileDir(file_path):
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok = True)

def ensureDir(directory):
    os.makedirs(directory, exist_ok = True)

def getCategoriesFromDirs():
    categories = []
    for dirname in os.listdir("data"):
        if os.path.isdir(os.path.join("data", dirname)) and not dirname.startswith("."):
            categories.append(dirname)
    return categories

def getSongsFromCatDir(category):
    songs = []
    for songname in os.listdir(os.path.join("data", category)):
        if songname.endswith(".sng"):
            songs.append(songname)
    return songs