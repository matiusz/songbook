import songJSONmaker

songJSONmaker.main()

import songbookTeXmaker

songbookTeXmaker.main()

import os

texcompile = "pdflatex songbook.tex"
os.system(texcompile)

import tocEdit

tocEdit.main()

os.system(texcompile)

auxFiles = ["songbook.tex", "songbook.toc", "songbook.aux", "songbook.fdb_latexmk", "songbook.ffs", "songbook.log", "songbook.synctex.gz", "songbook.fls", "songlist.toc"]

for auxFil in auxFiles:
    try:
        os.remove(auxFil)
    except FileNotFoundError:
        pass
    except Exception as ex:
        raise ex