  # songbook

  ## songJSONmaker.py

  Allows converting songs from text to JSON to prepare them for later processing into TeX file. List of categories is based on directories located in current working directory - if you want to add new cateogry simple create a new directory. Song JSON is saved with a <songTitle>.sng into the respective folder.

  ## songbook.py

  Reads .sng files from all the subdirectories in current working directory and converts them to single tex file. Currently both categories and songs in them are sorted          alphabetically.
  
  ## Requirements
  
  - Made using Python 3.9, should be compatible with most 3.x versoins.
  - PySide6 for Python
  - paracol for LaTeX
