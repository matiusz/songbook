import logging
import sys
def loggerSetup():
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.WARN)
    fileHandler = logging.FileHandler("songbook-py.log", mode = 'a', encoding= 'utf-8')
    fileHandler.setLevel(logging.INFO)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(name)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        handlers=[consoleHandler, fileHandler])
loggerSetup()
