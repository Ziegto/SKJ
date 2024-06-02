"""
Naimplementujte třídu Knihovna.
Knihovna obsahuje databázi knih, ke každé knize si udržuje počet dostupných kopií.

Metody, které máte naimplementovat a ukázka použití:
    knihovna = Knihovna()

    # Přidá knihu do knihovny
    knihovna.pridej_knihu("Harry Potter")
    knihovna.pridej_knihu("Harry Potter")
    knihovna.pridej_knihu("Lord of the Rings")
    knihovna.pridej_knihu("Artemis Fowl")


    # Pokud je v knihovně alespoň jedna kopie dané knihy, tak se jedna kopie z knihovny odebere a funkce vrátí True.
    # Pokud v knihovně daná kniha není, funkce vrátí False.
    knihovna.vypujc_knihu("Lord of the Rings") # True

    # Vrátí celkový počet všech kopií všech knih, které jsou v knihovně.
    knihovna.vrat_pocet_kopii() # 3

    # Vrátí knihu, která má v knihovně nejvíce kopií.
    # Pokud je takových knih více, vraťte libovolnou z nich.
    # Pokud v knihovně žádná kniha není, vraťte None.
    knihovna.vrat_nejcetnejsi_knihu() # "Harry Potter"
"""


class Knihovna:
    def __init__(self):
        self.databaze = {}

    def pridej_knihu(self, nazev):
        if nazev not in self.databaze:
            self.databaze[nazev] = 1
        else:
            self.databaze[nazev] += 1

    def vypujc_knihu(self, nazev):
        if nazev not in self.databaze:
            return False
        else:
            if self.databaze[nazev] > 0:
                self.databaze[nazev] -= 1
                return True
            else:
                return False

    def vrat_pocet_kopii(self):
        return sum(self.databaze.values())

    def vrat_nejcetnejsi_knihu(self):
        if not self.databaze:
            return None
        nejcetnejsi_kniha = max(self.databaze, key=self.databaze.get)
        return nejcetnejsi_kniha


knihovna = Knihovna()
print(knihovna.vypujc_knihu("Gang of Four"))  # false
print(knihovna.vrat_pocet_kopii())  # 0
print("\n")
knihovna.pridej_knihu("Gang of Four")
knihovna.pridej_knihu("Compilers")
print(knihovna.vrat_pocet_kopii())  # 2
print("\n")
print(knihovna.vypujc_knihu("Gang of Four"))  # true
print(knihovna.vypujc_knihu("Gang of Four"))  # false
print(knihovna.vrat_pocet_kopii())  # 1
print(knihovna.vrat_nejcetnejsi_knihu())  # Compilers
print("\n")
knihovna.pridej_knihu("Compilers")
print(knihovna.vrat_pocet_kopii())  # 2
print("\n")
print(knihovna.vypujc_knihu("Compilers"))  # true
print(knihovna.vypujc_knihu("Compilers"))  # true
print(knihovna.vypujc_knihu("Compilers"))  # false
print(knihovna.vrat_pocet_kopii())  # 0
print("\n")
knihovna.pridej_knihu("Computer architecture")
knihovna.pridej_knihu("Python for beginners")
knihovna.pridej_knihu("Operating systems")
knihovna.pridej_knihu("Python for beginners")
knihovna.pridej_knihu("Computer architecture")
knihovna.pridej_knihu("Python for beginners")
print(knihovna.vrat_nejcetnejsi_knihu())  # "Python for beginners"

"""
Otevřete CSV soubor na zadané cestě a načtěte z něj údaje.
Spočítejte průměrný počet bodů pro každý předmět v souboru a vraťte jej z funkce jako slovník
{předmět: průměrný počet bodů}.

CSV soubor má následující formát:
jmeno,predmet,body

Příklad:
Jan Novák,SPJA,16
Anna Melíšková,UDBS,8
Karel Pěchota,UDBS,30
Jaroslav Němec,SPJA,6

Ze souboru výše by měl vyjít slovník
{
 "SPJA": 11,
 "UDBS": 19
}
"""


def prumer(path):
    body_dict = {}
    predmety_dict = {}

    with open(path, "r") as file:
        for line in file:
            predmet = line.strip().split(",")[1]
            body = int(line.strip().split(",")[2])

            if predmet not in body_dict:
                body_dict[predmet] = body
                predmety_dict[predmet] = 1
            else:
                body_dict[predmet] += body
                predmety_dict[predmet] += 1

        prumery_dict = {}
        for predmet, body_sum in body_dict.items():
            prumery_dict[predmet] = body_sum / predmety_dict[predmet]

    print(prumery_dict)


prumer("data.csv")

"""
Vraťte True, pokud je zadaný řetězec palindrom (čte se stejně zepředu i pozpátku).

Příklad:
je_palindrom('a') # True
je_palindrom('aaa') # True
je_palindrom('aba') # True
je_palindrom('abc') # False
"""


def je_palindrom(text):
    delka = len(text)
    pulka = int(delka / 2)
    if text == '' or delka == 1:
        return True

    for i in range(pulka):
        if text[i] != text[delka - i - 1]:
            return False
    return True


print(je_palindrom(''))  # true
print(je_palindrom('a'))  # true
print(je_palindrom('aa'))  # true
print(je_palindrom('aaa'))  # true
print(je_palindrom('aba'))  # true
print(je_palindrom('abc'))  # false
print(je_palindrom('abcd'))  # false
print(je_palindrom('palindrom'))  # false
