import os

from src import ToCedit

from src.obj.Config import config

from src.tools.loggerSetup import logging

logger = logging.getLogger(__name__)


def main():
    '''Compiles the tex file into a pdf using pdflatex'''
    songbookTitle = config.outputFile
    inFile = f"{songbookTitle}.tex"
    outFile = f"{songbookTitle}.pdf"
    texcompile = f"pdflatex {inFile}"
    logger.info(f"Compiling {inFile} to {outFile}")
    if os.system(texcompile) != 0:
        logger.error("Command pdflatex exited with error")
        raise ModuleNotFoundError(texcompile)
    logger.info(f"PDF compiled successfully")
    if not config.devSettings.get('singleCompile', False):
        ToCedit.main()
        logger.info(f"Running second compilation...")
        os.system(texcompile)
        ToCedit.main()
        logger.info(f"Running third compilation...")
        os.system(texcompile)

    if config.devSettings.get('keepAuxOut', False):
        auxFiles = [f"{songbookTitle}.tex", f"{songbookTitle}.toc", f"{songbookTitle}.aux", f"{songbookTitle}.fdb_latexmk",
                    f"{songbookTitle}.ffs", f"{songbookTitle}.log", f"{songbookTitle}.synctex.gz", f"{songbookTitle}.fls",
                    f"{songbookTitle}_list.toc", f"{songbookTitle}.out"]
        logger.debug("Removing auxiliary files...")
        for auxFil in auxFiles:
            try:
                pass
                os.remove(auxFil)
            except FileNotFoundError:
                pass
    return outFile


if __name__ == "__main__":
    main()
