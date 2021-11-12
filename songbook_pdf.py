from src import TeXcompile, songbookTeXmaker
import sys
import os

songbookTexFile = songbookTeXmaker.main()
try:
    songbookPdfFile = TeXcompile.main()
except ModuleNotFoundError:
    sys.exit("Error generating pdf from tex, please check if pdflatex is installed or if .tex file was successfully generated.")

else:
    print(f"PDF generated at {os.path.join(os.getcwd(), songbookPdfFile)}")
