import songJSONmaker

songJSONmaker.main()

import songbookTeXmaker

songbookTeXmaker.main()

import os

texcompile = "pdflatex songbook.tex"
os.system(texcompile)
os.system(texcompile)