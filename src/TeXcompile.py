import os

from src import ToCedit

from src.obj.Config import config


def main():
    songbookTitle = config.outputFile
    inFile = f"{songbookTitle}.tex"
    outFile = f"{songbookTitle}.pdf"
    texcompile = f"pdflatex {inFile}"
    if os.system(texcompile) != 0:
        raise ModuleNotFoundError(texcompile)

    if not config.devSettings['singleCompile']:
        ToCedit.main()
        os.system(texcompile)
        ToCedit.main()
        os.system(texcompile)

    if not config.devSettings['keepAuxOut']:
        auxFiles = [f"{songbookTitle}.tex", f"{songbookTitle}.toc", f"{songbookTitle}.aux", f"{songbookTitle}.fdb_latexmk",
                    f"{songbookTitle}.ffs", f"{songbookTitle}.log", f"{songbookTitle}.synctex.gz", f"{songbookTitle}.fls",
                    f"{songbookTitle}_list.toc", f"{songbookTitle}.out"]
        for auxFil in auxFiles:
            try:
                pass
                os.remove(auxFil)
            except FileNotFoundError:
                pass
    return outFile


if __name__ == "__main__":
    main()
