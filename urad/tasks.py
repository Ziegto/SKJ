def frequent_visitors(path: str):
    days_counts = [0] * 7
    visitor_counts = {}

    with open(path, 'r') as file:
        for index, line in enumerate(file):
            day_index = index % 7
            visitor_today = set(line.strip().split(","))
            for visitor in visitor_today:
                if visitor:
                    visitor = int(visitor)
                    if visitor not in visitor_counts:
                        visitor_counts[visitor] = 0
                    visitor_counts[visitor] += 1
                    days_counts[day_index] += 1
    sorted_visitors = sorted(visitor_counts.items(), key=lambda x: (-x[1], -x[0]))

    return tuple(days_counts), tuple(sorted_visitors)


"""
Úkol 1

Sociální úřad je přetížený. Potřebuje identifikovat, v které dny jej navštěvuje nejvíce lidí,
a také najít osoby, které ho navštěvují nejčastěji, aby jim doporučil zřízení datové schránky.
Pomozte mu naimplementováním funkce `frequent_visitors`.

Funkce obdrží cestu k textovému souboru v parametru `path`. V souboru budou chronologicky seřazené
záznamy o návštěvách úřadu. Každý řádek reprezentuje jeden den, dny následují po sobě bez mezer
a první den je vždy pondělí. Druhý řádek tedy bude úterý, třetí středa, ..., sedmý neděle, osmý
opět pondělí atd.

Na každém řádku je seznam čísel oddělených čárkou. Každé číslo identifikuje jednoho návštěvníka,
čísla se mohou v daném dni opakovat (stejný návštěvník může za jeden den přijít vícekrát).
Každé číslo unikátně identifikuje jednoho návštěvníka (můžete ho chápat např. jako rodné číslo).

Příklad souboru:
```
1,8,1,6,7
2,4,3
7
9,12

8,3,7,15
2
3,4
```
Tento ukázkový soubor obsahuje záznamy o 8 dnech. První den (pondělí) přišli návštěvníci
1, 8, 6 a 7, v druhý den (úterý) návštěvníci 2, 4 a 3 atd. V pátý den (pátek) úřad nenavštívil
nikdo. V osmý den (pondělí) úřad navštívili návštěvníci 3 a 4.

Vaším úkolem je vypočítat dva údaje, celkový počet unikátních návštěv v jednotlivých dnech
týdne (CPUN-D), a celkový počet unikátních návštěv pro jednotlivé návštěvníky (CPUN-N).

Unikátní návštěvy znamenají, že při výpočtu byste měli brát v potaz vždy pouze první návštěvu
konkrétního návštěvníka v daném dni. Jinak řečeno, pokud nějaký návštěvník navštíví úřad více
než jednou ve stejném dni, tak tyto další návštěvy zcela ignorujte.

Pro výpočet CPUN-D spočítejte pro každý den v týdnu, kolik unikátních návštěv celkem bylo v
tomto dni. Výsledek reprezentujte jako n-tici sedmi čísel (počet návštěv pro pondělí, úterý,
středu, ...).

Pro výpočet CPUN-N pro každého návštěvníka vypočítejte, kolik měl celkem unikátních návštěv úřadu.
Výsledek reprezentujte jako n-tici dvojic (ID návštěvníka, počet unikátních návštěv) seřazenou
sestupně dle počtu unikátních návštěv (v případě shody počtu návštěv řaďte sestupně podle ID
návštěvníka).

Z funkce poté vraťte dvojici (CPUN-D, CPUN-N).
Výsledek funkce může vypadat např. takto:
```
(
    (3, 2, 2, 1, 0, 1, 1),
    (
        (1, 5),
        (6, 4),
        (3, 1)
    )
)
```
To by znamenalo, že v pondělí úřad navštívily 3 unikátní návštěvy, v úterý 2, v neděli 1 atd.
Návštěvník s ID 1 měl 5 unikátních návštěv, návštěvník s ID 6 měl 4 unikátní návštěvy a
návštěvník s ID 3 měl jednu unikátní návštěvu.

Ukázkové výstupy pro vstupní soubory `test*.txt` naleznete v souboru `tests.py`.
"""


class CounterManager:
    def __init__(self, prepazky):
        self.prepazky = prepazky
        self.fronty = self.initialize_fronty(prepazky)
        self.odbaveni_navstevnici = [0] * len(prepazky)

    @staticmethod
    def initialize_fronty(prepazky):
        fronty = []
        for _ in prepazky:
            fronty.append([])
        return fronty

    def queue_visitor(self, pozadavky):
        vhodne_prepazky = []
        for idx, prep in enumerate(self.prepazky):
            if all(p in prep for p in pozadavky) and len(self.fronty[idx]) < 5:
                vhodne_prepazky.append((idx, len(self.fronty[idx])))

        if not vhodne_prepazky:
            raise Exception("No suitable counter found or all queues are full")

        vybrana_prepazka = min(vhodne_prepazky, key=lambda x: (x[1], x[0]))[0]
        self.fronty[vybrana_prepazka].append(pozadavky)
        return vybrana_prepazka + 1

    def counter_advance(self, id):
        if not 1 <= id <= len(self.prepazky):
            raise Exception("Invalid counter ID")

        idx = id - 1
        if not self.fronty[idx]:
            raise Exception("No visitors in the queue")

        self.fronty[idx].pop(0)
        self.odbaveni_navstevnici[idx] += 1

    def counter_queue_sizes(self):
        return [len(fronta) for fronta in self.fronty]

    def counter_finished_visitors(self):
        return self.odbaveni_navstevnici



"""
Třída bude spravovat několik přepážek.
    - Přepážky jsou číslovány postupně od 1 do N.
    - Přepážka obsahuje seznam činností, které lze na přepážce vyřídit (např. vyřídit pas
    nebo občanku).
    - Přepážka má frontu návštěvníků, kteří čekají na odbavení.
        - Maximální velikost fronty je 5.
        - Pokud je fronta zaplněna, nelze už přidat dalšího návštěvníka do fronty.
    - Přepážka si pamatuje, kolik návštěvníků už odbavila.
    - Při vytvoření třídy jsou všechny fronty přepážek prázdné.

Když na úřad přijde návštěvník, tak třída určí, jestli existuje přepážka, která dokáže splnit
všechny jeho požadavky, a vybere mu přepážku v závislosti na jejich obsazenosti, pokud je ještě
na nějaké přepážce volno.
Přepážku volte tak, aby byla schopna splnit všechny požadavky návštěvníka a měla co nejmenší
aktuální velikost fronty. V případě, že by tyto podmínky splňovalo více přepážek, vyberte
přepážku s nejnižším ID.

Třída bude poskytovat následující rozhraní:
```python
# Vytvoření správce s dvěma přepážkami.
# První přepážka umí vyřizovat pasy, druhá pasy i občanky.
manager = CounterManager([["pas"], ["pas, "občanka"]])

# Na úřad přišel zákazník, který potřebuje vyřídit občanku
# Jediná přepážka, která ho může obsloužit, je přepážka s ID 2
queue_id = manager.queue_visitor(["občanka"])
assert queue_id == 2

# Pokud neexistuje přepážka, která by zvládla vyřídit požadavky návštěvníka, vyhodí metoda
# libovolnou výjimku
# Pokud už by nebyla dostupná přepážka s frontou menší než 5 návštěvníků, vyhodí metoda
# libovolnou výjimku
# manager.queue_visitor(["pas", "občanka", "řidičák"]) # vyhodí výjimku

# Odbaví jednoho návštěvníka na přepážce s daným ID.
# Pokud přepážka s tímto ID neexistuje nebo v její frontě není žádný návštěvník, metoda vyhodí
# libovolnou výjimku
manager.counter_advance(1)

# Vrátí seznam čísel, které udávají, kolik lidí je zrovna ve frontě na jednotlivých přepážkách
manager.counter_queue_sizes()

# Vrátí seznam čísel, které udávají, kolik lidí je už bylo odbaveno na jednotlivých přepážkách
manager.counter_finished_visitors()
```
"""
