from posixpath import dirname
from updateFormat import isSongCategoryDir
import os
dataFolder1 = "data"
dataFolder2 = "dataAll"

songsDict1 = {songDir: os.listdir(os.path.join(dataFolder1, songDir)) for songDir in os.listdir(dataFolder1) if isSongCategoryDir(songDir)}
songsDict2 = {songDir: os.listdir(os.path.join(dataFolder2, songDir)) for songDir in os.listdir(dataFolder2) if isSongCategoryDir(songDir)}

for k in songsDict1.keys():
    for song in songsDict1[k]:
        if not song in songsDict2[k]:
            print(f"Song {song} from in category {k} is in folder {dataFolder1} but not in {dataFolder2}")

for k in songsDict2.keys():
    for song in songsDict2[k]:
        if not song in songsDict1[k]:
            print(f"Song {song} in category {k} is in folder {dataFolder2} but not in {dataFolder1}")