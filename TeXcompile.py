def main():
    import os

    texcompile = "pdflatex songbook.tex"
    os.system(texcompile)

    import ToCedit

    ToCedit.main()

    os.system(texcompile)

    auxFiles = ["songbook.tex", "songbook.toc", "songbook.aux", "songbook.fdb_latexmk", "songbook.ffs", "songbook.log", "songbook.synctex.gz", "songbook.fls", "songlist.toc", "songbook.out"]

    for auxFil in auxFiles:
        try:
            os.remove(auxFil)
        except FileNotFoundError:
            pass
        except Exception as ex:
            raise ex

if __name__=="__main__":
    main()