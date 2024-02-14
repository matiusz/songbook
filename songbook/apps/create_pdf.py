from ..src.tools.loggerSetup import logging

from src import TeXcompile, songbookTeXmaker
import sys
import os


def main():
    logger = logging.getLogger(__name__)

    songbookTexFile = songbookTeXmaker.main()
    try:
        songbookPdfFile = TeXcompile.main()
    except ModuleNotFoundError:
        sys.exit("Error generating pdf from tex, please check if pdflatex is installed or if .tex file was successfully generated.")

    else:
        logger.info(f"PDF generated at {os.path.join(os.getcwd(), songbookPdfFile)}")

if __name__ == '__main__':
    main()