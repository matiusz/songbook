  # songbook
  
  ## songbook.py
  
  Script for running all the parts of the application.

  ## songJSONmaker.py

  GUI with options for song lookup and adding new categories and songs and editing existing songs.

  ## songbookTeXmaker.py

  Creates .tex file from added songs

  ## TeXcompile.py

  Compiles the .tex file, generates secondary ToC and recompiles everything two more times to ensure correct page numbering.

  ## Requirements
  
  - Python 3.7+
  - PySide6 (pip install PySide6) - GUI module
  - aiofiles (pip install aiofiles) - module for async I/O operations on files
  - pdfTeX (included with e.g. https://miktex.org/) - required for .tex -> .pdf compilation
