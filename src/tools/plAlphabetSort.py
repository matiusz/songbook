import locale

locale.setlocale(locale.LC_ALL, "pl_PL")

def plSortKey(letter):
    return locale.strxfrm(letter)
