import locale

locale.setlocale(locale.LC_ALL, "pl_PL.UTF-8")

def plSortKey(letter):
    return locale.strxfrm(letter)

for lang in locale.locale_alias.values():
    print(lang)