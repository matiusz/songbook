  # songbook
  
  ## songbook

  Songbook is an easy to use tool for creating songbooks where each song is represented by a different file, allowing them to be easily shared or moved between different songbooks. It has it's own display module or it can generate LaTeX files and compile them to pdf.

  ## Configuration

  ### pdfSettings

  format - e.g. a4paper, a5paper\
  sides - oneside/twoside - if twoside is set pdf will have inner and outer margins and will include a blank page if chapter would start on an even page otherwise\
  textFieldSize - width and height of area text area\
  margins 
  - horizontal - inner in case of twoside option, left otherwise
  - vertical - top margin
  
  fontSize - basic size of the font, supports sizes 10, 11, 12\
  lyricsFont, chordsFont - one of the fontcodes available e.g. here: https://www.overleaf.com/learn/latex/Font_typefaces#Reference_guide
  

  ## Requirements
  
  - Python 3.9+
  - PySide6 (pip install PySide6) - GUI module
  - aiofiles (pip install aiofiles) - module for async I/O operations on files
  - pdfTeX (included with e.g. https://miktex.org/) - required for .tex -> .pdf compilation
