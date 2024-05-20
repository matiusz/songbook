from flask_frozen import Freezer
from ..src.flask.flask_app import app
from ..src.obj.Songbook import Songbook
from ..src.tools.loggerSetup import logging
from ..src import songbookTeXmaker, TeXcompile

import os, sys, shutil

freezer = Freezer(app)
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html; charset=utf-8'
app.config['FREEZER_DESTINATION'] = os.path.join(os.getcwd(), "build")


def create_pdf():
    logger = logging.getLogger(__name__)

    songbookTexFile = songbookTeXmaker.main()
    try:
        songbookPdfFile = TeXcompile.main()
    except ModuleNotFoundError:
        sys.exit("Error generating pdf from tex, please check if pdflatex is installed or if .tex file was successfully generated.")
    else:
        logger.info(f"PDF generated at {os.path.join(os.getcwd(), songbookPdfFile)}")
        return songbookPdfFile


@freezer.register_generator
def start():
    sb = Songbook()
    for cat in sb.sb:
        for sng in sb.sb[cat]:
            yield {'category': cat, 'song': sng.title}


def main():
    freezer.freeze()
    songbookPdfFile = create_pdf()
    shutil.copy(songbookPdfFile, os.path.join("build/static", songbookPdfFile))



if __name__ == '__main__':
    main()