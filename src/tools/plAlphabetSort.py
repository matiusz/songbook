import locale

locale.setlocale(locale.LC_ALL, "")

def plSortKey(letter):
    return locale.strxfrm(letter)

for lang in locale.locale_alias.values():
    print(lang)