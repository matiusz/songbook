import locale

locale.setlocale(locale.LC_ALL, "pl_PL.UTF-8")


def plSortKey(letter: str) -> str:
    return locale.strxfrm(letter)
