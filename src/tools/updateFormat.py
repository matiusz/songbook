
import json
from src.obj.Config import config
from src.obj.Songbook import Song
import os, asyncio, aiofiles
from src.tools.dirTools import ensureDir
from pathlib import Path


def isSongCategoryDir(dirname):
    return os.path.isdir(os.path.join(config.dataFolder, dirname)) and not (dirname.startswith((".", "_")))

async def reformatAll():
    tasks = [reformatCategory(os.path.join(config.dataFolder, dirname))
             for dirname in os.listdir(config.dataFolder) if isSongCategoryDir(dirname)]
    categories = await asyncio.gather(*tasks)
    return categories


async def reformatCategory(dirpath):
    tasks = [reformatSong(dirpath, filename) for filename in os.listdir(dirpath) if filename.endswith(".sng")]
    songs = await asyncio.gather(*tasks)
    return songs


async def reformatSong(dirpath, filename):
    async with aiofiles.open(os.path.join(dirpath, filename), "r") as f:
        try:
            song = Song.loadFromDict(json.loads(await f.read()))
            song.save()
        except UnicodeDecodeError:
            print(filename)

async def resaveAll():
    ensureDir("dataNEW")
    tasks = [resaveCategory(os.path.join(config.dataFolder, dirname))
             for dirname in os.listdir(config.dataFolder) if isSongCategoryDir(dirname)]
    categories = await asyncio.gather(*tasks)
    return categories

async def resaveCategory(dirpath):
    ensureDir(os.path.join("dataNEW", Path(dirpath).stem)) 
    tasks = [resaveSong(dirpath, filename) for filename in os.listdir(dirpath) if filename.endswith(".sng")]
    songs = await asyncio.gather(*tasks)
    return songs

async def resaveSong(dirpath, filename):
    config.dataFolder = "data"
    song = Song.loadFromFile(os.path.join(dirpath, filename))
    config.dataFolder = "dataNEW"
    song.save()

asyncio.run(resaveAll())