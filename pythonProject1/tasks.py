"""
Úkol 1 (15 bodů)

Jednotka SG-11 se ztratila! Je třeba pro ni vyslat záchrannou misi.
Bohužel není jasné, kde přesně se ztratila, k dispozici jsou pouze útržky nouzových signálů z různých bodů,
kde by jednotka mohla být.

Pomozte najít jednotku SG-11 tím, že naimplementujete funkci spocti_krychli.
Funkce ze souboru na zadané cestě načte 3D souřadnice bodů a najde nejmenší krychli, která ohraničuje tyto
souřadnice (stačí naleznout minimální/maximální souřadnice na všech osách).
Každý řádek v souboru reprezentuje jeden 3D bod, jednotlivé souřadnice jsou odděleny čárkou.
Funkce poté vrátí objem tohoto krychle, aby šlo zjistit, jak velký prostor je nutný prohledat k nalezení jednotky.

Příklad (ukázka souboru soubor_souradnice):
1,2,3
-5,8,-20
2,6,0

spocti_krychli("souradnice_test.txt") # 966
# minimum první souřadnice je -5, maximum je 2, takže první rozměr je 7, obdobně lze naleznout zbylé rozměry
"""
def spocti_krychli(soubor_souradnice):
    with open(soubor_souradnice, "r") as f:
        content = f.read()

    lines = content.strip().split()

    first_x, first_y, first_z = map(float, lines[0].split(','))

    min_x, max_x = first_x, first_x
    min_y, max_y = first_y, first_y
    min_z, max_z = first_z, first_z

    for line in lines[1:]:
        x, y, z = map(float, line.split(','))
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)

    rozmery = (max_x - min_x) * (max_y - min_y) * (max_z - min_z)

    return rozmery


spocti_krychli("souradnice_test.txt")

"""
Úkol 2 (10 bodů)

Pro nalezení SG-11 je třeba vyřešit další problém - nefunguje ovládací panel k Hvězdné bráně.
Naštěstí Samantha Carterová navrhla dočasné řešení - pomozte jí vytvořit softwarový modul pro ovládání brány.

Naimplementujte třídu OvladaciPanel, která obdrží seznam znaků na panelu.
Znaky jsou uspořádané do kruhu, jeden ze znaků je vždy aktivní (na začátku to bude nultý znak v seznamu).
Uživatel může měnit aktivní znak pomocí pohybu doleva nebo doprava.
Nezapomeňte, že znaky jsou uspořádány do kruhu, lze je tak všechny projet pohybem pouze doleva nebo pouze doprava.

Uživatel může aktivní znak zadat, čímž dojde k přidání aktivního znaku do adresy.
Po přidání všech požadovaných znaků může vytočit adresu (při vytočení panel vrátí seznam všech navolených
znaků v pořadí, ve kterém byly navoleny).

Příklad:
panel = OvladaciPanel(["A", "B", "C"]) # nejprve je aktivní znak "A"
panel.posun_doprava() # nyní je aktivní znak "B"
panel.zadej_znak()    # znak "B" je přidán do vytočené adresy
panel.posun_doprava() # nyní je aktivní znak "C"
panel.posun_doprava() # nyní je aktivní znak "A"
panel.zadej_znak()    # znak "A" je přidán do vytočené adresy
panel.posun_doleva()  # nyní je aktivní znak "C"
panel.zadej_znak()    # znak "C" je přidán do vytočené adresy
panel.vytoc_adresu()  # vrátí ["B", "A", "C"]
"""


class OvladaciPanel:
    def __init__(self, znaky):
        self.znaky = znaky
        self.aktivniIndex = 0
        self.navoleneZnaky = []

    def posun_doprava(self):
        if self.aktivniIndex >= len(self.znaky) - 1:
            self.aktivniIndex = 0
        else:
            self.aktivniIndex += 1

    def posun_doleva(self):
        if self.aktivniIndex <= 0:
            self.aktivniIndex = len(self.znaky) - 1
        else:
            self.aktivniIndex -= 1

    def zadej_znak(self):
        self.navoleneZnaky.append(self.znaky[self.aktivniIndex])

    def vytoc_adresu(self):
        return self.navoleneZnaky


def zkouska(soubor):
    auticka_dict = {}
    with open(soubor, "r") as file:
        for line in file:
            auto_line = line.strip().split()
            for auto in auto_line:
                if auto in auticka_dict:
                    auticka_dict[auto] += 1
                else:
                    auticka_dict[auto] = 1

    sort = sorted(auticka_dict.items(), key=lambda x: (-x[1], x[0]))
    print(sort)


zkouska("planety_test.txt")

"""
Úkol 3 (15 bodů)

Nyní už víme přibližnou lokaci SG-11 a máme funkční ovládací panel, zbývá určit přesnou polohu jednotky.
V operačním deníku jednotky jsou adresy planet, které SG-11 navštívila, z těchto informací a přibližné lokace
jednotky by mělo jít dohledat, kde se jednotka přesně nachází.

Naimplementujte funkci nejcastejsi_glyfy.
Funkce ze souboru na zadané cestě načte adresy planet, kam SG-11 cestovala.
Každá adresa (řádek v souboru) je tvořena několika slovy (glyfy) oddělenými mezerou.
Spočítejte, kolikrát se jednotlivé glyfy vyskytují v souboru a vraťte z funkce seznam dvojic (glyf, počet výskytů)
seřazený sestupně dle počtu výskytů jednotlivých glyfů.
Pokud budou mít dva nebo více glyfů stejný počet výskytů, seřaďte je lexikograficky vzestupně dle jejich názvu
("dle abecedy").
V jedné adrese se konkrétní glyf může vyskytovat maximálně jednou.

Příklad (ukázka souboru soubor_adresy):
Crater Taurus Virgo Capricornus Auriga Eridanus Gemini
Taurus Crater Lynx Hydra Auriga Sagittarius Orion
Crater Aries Taurus Scutum Sagittarius Gemini Norma

nejcastejsi_glyfy("planety_test.txt")
# [
#  ('Crater', 3), ('Taurus', 3), ('Auriga', 2), ('Gemini', 2), ('Sagittarius', 2), ('Aries', 1),
#  ('Capricornus', 1), ('Eridanus', 1), ('Hydra', 1), ('Lynx', 1), ('Norma', 1), ('Orion', 1), ('Scutum', 1),
#  ('Virgo', 1)
# ]
"""


def nejcastejsi_glyfy(soubor_adresy):
    glyfy_dict = {}

    with open(soubor_adresy, "r") as file:
        for line in file:
            glyfy = line.strip().split()
            for glyf in glyfy:
                if glyf in glyfy_dict:
                    glyfy_dict[glyf] += 1
                else:
                    glyfy_dict[glyf] = 1
    sorted_glyfy = sorted(glyfy_dict.items(), key=lambda x: (-x[1], x[0]))
    return sorted_glyfy


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
        if nazev in self.databaze:
            self.databaze[nazev] += 1
        else:
            self.databaze[nazev] = 1

    def vypujc_knihu(self, nazev):
        if nazev in self.databaze and self.databaze[nazev] > 0:
            self.databaze[nazev] -= 1
            return True
        else:
            return False

    def vypis(self):
        return self.databaze

    def vrat_pocet_kopii(self):
        return len(self.databaze)

    def vrat_nejcetnejsi_knihu(self):
        if len(self.databaze) > 0:
            nejcetnejsi = sorted(self.databaze.items(), key=lambda x: (-x[1], x[0]))
            nej = nejcetnejsi[0][0]
            return nej
        else:
            return None


def nejvetsi_poklad(soubor_adresy):
    artefakty_dict = {}

    with open(soubor_adresy, "r") as file:
        for line in file:
            artefakty = line.strip().split()
            for artefakt in artefakty:
                if artefakt in artefakty_dict:
                    artefakty_dict[artefakt] += 1
                else:
                    artefakty_dict[artefakt] = 1

    sort_artefakty = sorted(artefakty_dict.items(), key=lambda x: (x[1], x[0]))
    houby = sort_artefakty.pop()
    return houby


def analyzuj_logy(soubor):
    logy_dict = {}

    with open(soubor, "r") as file:
        for line in file:
            log = int(line.strip().split()[2])
            if log in logy_dict:
                logy_dict[log] += 1
            else:
                logy_dict[log] = 1

    serazene_logy = sorted(logy_dict.items(), key=lambda x: (-x[1], -x[0]))

    return serazene_logy


def je_palindrom(text):
    delka = len(text) - 1
    pulka = int(len(text) / 2)
    index = False

    if delka < 2:
        index = True
    else:
        for i in range(pulka):
            if not text[i] == text[delka - i]:
                index = False
            else:
                index = True

    return index


def analyzuj_zpravy(soubor):
    zpravy_dict = {}

    with open(soubor, "r") as file:
        for line in file:
            _, zprav = line.strip().split(",", 1)
            for slovo in zprav.split():
                if slovo in zpravy_dict:
                    zpravy_dict[slovo] += 1
                else:
                    zpravy_dict[slovo] = 1

    sort_zpravy = sorted(zpravy_dict.items(), key=lambda x: (-x[1], x[0]))
    return sort_zpravy


# Nyní můžete funkci zavolat a měla by fungovat bez chyby
# print(analyzuj_zpravy("zpravy.txt"))


def kokot(soubor):
    dict = {}

    with open(soubor, "r") as file:
        for line in file:
            koko = line.strip().split()
            for kok in koko:
                if kok in dict:
                    dict[kok] += 1
                else:
                    dict[kok] = 1
    sort = sorted(dict.items(), key=lambda x: (-x[1], x[0]))

    nejvic3 = [sort[0], sort[len(sort) - 1]]

    print(nejvic3)

# kokot("artefakty.txt")
