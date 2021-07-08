  # songbook
  
  ## songbook.py
  
  Script for running all the parts of the application.

  ## songJSONmaker.py

  Allows creating categories with pictures and converting songs from text to JSON to prepare them for later processing into TeX file. Song JSONs are saved with a .sng extension into respective directories.

  ## songbookTeXmaker.py

  Reads .sng files from all the subdirectories in current working directory and converts them to single tex file. Categories can be sorted manually by modifying generated categories.cfg file. Songs within each category are sorted alphabetically.
  
  ## Requirements
  
  - Made using Python 3.9, should be compatible with most 3.x versoins.
  - PySide6 for Python for generating song JSONs
  - pdfTeX is required for the automated script
