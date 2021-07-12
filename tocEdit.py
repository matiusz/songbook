def main():
    filename = 'songbook.toc'

    with open(filename, 'rb') as f:
        content = [line.decode('utf-8') for line in f.readlines() if "section" in line.decode("utf-8")]

    with open("songlist.toc", 'wb') as f:
        for i in sorted(content):
            f.write(i.encode("utf-8"))


if __name__=="__main__":
    main()