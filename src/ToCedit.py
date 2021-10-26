from src.tools.plAlphabetSort import plSortKey

from src.obj.Config import config

def main():
    filename = f'{config.outputFile}.toc'

    with open(filename, 'rb') as f:
        content = [line.decode('utf-8') for line in f.readlines() if "section" in line.decode("utf-8")]

    with open(f"{config.outputFile}_list.toc", 'wb') as f:
        for i in sorted(content, key=plSortKey):
            f.write(i.encode("utf-8"))


if __name__=="__main__":
    main()
