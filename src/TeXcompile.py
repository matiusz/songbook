import os

from src import ToCedit

def main():
    songbookTitle = "songbook"
    inFile = f"{songbookTitle}.tex"
    outFile = f"{songbookTitle}.pdf"
    texcompile = f"pdflatex {inFile}"
    os.system(texcompile)

    ToCedit.main()

    os.system(texcompile)
    os.system(texcompile)
    #auxFiles = []
    auxFiles = ["songbook.tex", "songbook.toc", "songbook.aux", "songbook.fdb_latexmk", "songbook.ffs", "songbook.log", "songbook.synctex.gz", "songbook.fls", "songlist.toc", "songbook.out"]

    for auxFil in auxFiles:
        try:
            os.remove(auxFil)
        except FileNotFoundError:
            pass
    return outFile

if __name__=="__main__":
    main()