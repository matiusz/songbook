  # songbook
  
  ## songbook.py
  
  Script for running all the parts of the application.
  
  Opens GUI which enables creating and editing songs. After GUI is closed it creates a .tex file, then compiles it to pdf and removes any auxiliary files.

  ## Requirements
  
  - Python 3.7+
  - PySide6 (pip install PySide6) - GUI module
  - aiofiles (pip install aiofiles) - module for async I/O operations on files
  - pdfTeX (included with e.g. https://miktex.org/) - required for .tex -> .pdf compilation
