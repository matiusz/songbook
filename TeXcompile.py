import ToCedit
import os

def main():

    texcompile = "pdflatex songbook.tex"
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

if __name__=="__main__":
    main()