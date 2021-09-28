import locale

locale.setlocale(locale.LC_ALL, "")

def plSortKey(letter):
    return locale.strxfrm(letter)
