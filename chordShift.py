import re

def shiftChords(chords, diff):
    majChords = ['C', 'Cis', 'D', 'Dis', 'E', 'F', 'Fis', 'G', 'Gis', 'A', 'B', 'H']
    minChords = [ch.lower() for ch in majChords]
    chDict = {}
    chDict['add'] = 'add'
    chDict['sus'] = 'sus'
    for idx, ch in enumerate(majChords):
        chDict[ch] = majChords[(idx + diff) % len(majChords)]
    for idx, ch in enumerate(minChords):
        chDict[ch] = minChords[(idx + diff) % len(minChords)]
        
    pattern = re.compile('|'.join(sorted(chDict.keys(), key=len, reverse=True)))
    result = pattern.sub(lambda x: chDict[x.group()], chords)
    return result
