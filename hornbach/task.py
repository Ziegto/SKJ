def is_plant_reachable(file, target):
    with open(file, 'r') as f:
        lines = f.readlines()
        height, width = map(int, lines[0].strip().split())
        warehouse_map = [list(line.strip()) for line in lines[1:]]

    start_pos = None
    for i, row in enumerate(warehouse_map):
        for j, cell in enumerate(row):
            if cell == 'S':
                start_pos = (i, j)
                break
        if start_pos:
            break

    if not start_pos:
        return False

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = [start_pos]
    visited = set([start_pos])

    while queue:
        x, y = queue.pop(0)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < height and 0 <= ny < width:
                if (nx, ny) not in visited:
                    if warehouse_map[nx][ny] == target:
                        return True
                    if warehouse_map[nx][ny] == ' ':
                        queue.append((nx, ny))
                        visited.add((nx, ny))

    return False


"""
    Úkol 1

    Ve skladu firmy Hornbach se porouchal systém pro správu skladu rostlin.
    Pomozte skladníkům naimplementováním funkce `is_plant_reachable`, která obdrží soubor s
    mapou skladu rostlin, a zjistí, jestli se lze ze startovního bodu s vozítkem dostat k
    cílové rostlině, či nikoliv.

    Parametr `file` bude obsahovat cestu k souboru s mapou skladu.
    - Na prvním řádku souboru naleznete rozměry skladu ve formátu `<výška> <šířka>`.
    - Na dalších řádcích poté bude uložena mapa skladu se zadanými rozměry.
    - Každá pozice v mapě je reprezentována jedním znakem.
        - Znak "S" reprezentuje startovní pozici vozítka. V mapě bude vždy právě jedna startovní pozice.
        - Znak " " (mezera) reprezentuje volné místo, kterým lze projet.
        - Jakýkoliv jiný znak označuje místo, kterým nelze projet, nebo cílovou rostlinu (viz níže).

    Parametr `target` obsahuje cílovou rostlinu, ke které se chceme dostat.
    - Cílová rostlina bude vždy reprezentována jedním znakem, který se nebude rovnat "S" ani " ".

    Funkce musí určit, zda je možné se ze startovní pozice vozítkem dostat k cílové rostlině
    pomocí povolených pohybů (viz níže).
    Pokud to je možné, funkce vrátí True.
    Pokud to není možné, funkce vrátí False.

    Pravidla pohybu vozítka:
    - Vozítko začíná na startovní pozici.
    - Vozítko se smí pohybovat pouze přes volná místa (reprezentována mezerami).
    - Vozítko se smí pohybovat pouze nahoru, dolů, doprava a doleva (nemůže se hýbat diagonálně).
    - Ujistěte se, že vozítko nevyjede ven z mapy!

    Příklad vstupního souboru:
    ```
    6 5
    xxx x
    zS  x
       Ox
     xxxx
    xL  x
    xxxxx
    ```
    Mapa tohoto skladu má 6 řádků a 5 sloupců.
    Startovní pozice je (1, 1).

    Pokud by funkce dostala s touto mapou cílovou rostlinu "O", měla by vrátit True (k rostlině se lze dostat).
    Pokud by funkce dostala s touto mapou cílovou rostlinu "L", měla by vrátit False (k rostlině se nelze dostat).
    Pokud by funkce dostala s touto mapou cílovou rostlinu např. "U", měla by vrátit False (taková rostlina ve skladu vůbec není).

    Ukázkové výstupy pro vstupní soubory `plants-<X>.txt` naleznete v souboru `tests.py`.
"""


class FlowerPotBelt:
    class FlowerPotBelt:
        def __init__(self, positions, max_load):
            self.positions = positions
            self.max_load = max_load
            self.belt = [None] * positions
            self.current_position = 0
            self.total_soil_weight = 0

        def place_flowerpot(self, max_weight):
            if self.belt[self.current_position] is not None:
                raise Exception("There is already a flowerpot at the current position.")
            self.belt[self.current_position] = {"max_weight": max_weight, "soil": {}}

        def add_soil(self, soil_type, weight):
            pot = self.belt[self.current_position]
            if pot is None:
                raise Exception("There is no flowerpot at the current position.")
            current_soil_weight = sum(pot["soil"].values())
            if current_soil_weight + weight > pot["max_weight"]:
                raise Exception("Not enough space in the flowerpot for the soil.")
            if self.total_soil_weight + weight > self.max_load:
                raise Exception("Adding this soil exceeds the belt's maximum load.")
            if soil_type in pot["soil"]:
                pot["soil"][soil_type] += weight
            else:
                pot["soil"][soil_type] = weight
            self.total_soil_weight += weight

        def get_pot(self):
            pot = self.belt[self.current_position]
            if pot is None:
                return None
            soil_info = tuple(sorted(pot["soil"].items()))
            return soil_info

        def take_pot(self):
            pot = self.belt[self.current_position]
            if pot is None:
                raise Exception("There is no flowerpot at the current position.")
            current_soil_weight = sum(pot["soil"].values())
            if current_soil_weight < pot["max_weight"] / 2:
                raise Exception("The flowerpot is not filled to at least half of its maximum weight.")
            self.total_soil_weight -= current_soil_weight
            self.belt[self.current_position] = None

        def move_right(self):
            self.current_position = (self.current_position + 1) % self.positions

        def move_left(self):
            self.current_position = (self.current_position - 1) % self.positions

    """
    Úkol 2

    Aby toho nebylo málo, kromě nefunkčního systému dnes ani do práce nepřišel stážista, který se
    stará o pás s květináči. Vytvořte třídu `FlowerPotBelt`, která za něj zaskočí.

    Vlastnosti třídy:
    Třída bude reprezentovat pás s N pozicemi pro květináče.
        - Pás má maximální zátěž, kterou může unést.
        - Obě dvě hodnoty (počet pozic a maximální zátěž) budou zadány v konstruktoru třídy.
    Pás si uchovává současnou pozici, nad kterou budou probíhat operace s květináči.
        - Pás umožní přepínat současnou pozici pomocí pohybů doleva a doprava.
        - Pás je zapojen do kruhu. Pokud např. dojde k pohybu doprava na pravém kraji pásu, tak se
          současná pozice posune na levý kraj pásu.
        Příklad pásu s 3 pozicemi (hranaté závorky označují současnou pozici):
            začáteční stav -> [K1] _ K2
            pohyb doprava  -> K1 [_] K2
            pohyb doprava  -> K1 _ [K2]
            pohyb doprava  -> [K1] _ K2
            pohyb doleva   -> K1 _ [K2]
    Na každé pozici pásu se může nacházet květináč, nebo může být pozice prázdná.
        - Pás umožní vložit na současnou pozici květináč, pokud je pozice prázdná.
        - Na začátku budou všechny pozice na pásu prázdné.
    Každý květináč bude obsahovat informaci o tom, jakou maximální hmotnost hlíny do něj lze vložit.
        - Pás umožní vložit do květináče na současné pozici zadané množství hlíny určitého typu.
            - Hlínu půjde vložit pouze tehdy, pokud v daném květináči bude dostatek místa, a zároveň
              pokud celková váha veškeré hlíny ve všech květináčích na pásu nepřesáhne jeho maximální zátěž.
        - Pás umožní získat informace o hlíně, která se nachází v květináči na současné pozici.
        - Pás umožní odebrat květináč na současné pozici, pokud je alespoň z poloviny zaplněn.

    Třída bude poskytovat následující rozhraní:
    ```python
    # Vytvoření pásu s 3 pozicemi a maximální zátěží 15 kg.
    belt = FlowerPotBelt(3, 15)

    # Umístění květináče s maximální hmotností 5 kg hlíny na současnou pozici.
    # - Pokud na současné pozici už je květináč, metoda vyhodí libovolnou výjimku.
    belt.place_flowerpot(5)

    # Přidání hlíny typu "soft" s váhou 2 kg do květináče na současné pozici.
    # - Pokud na současné pozici není květináč, metoda vyhodí libovolnou výjimku.
    # - Pokud se do květináče na současné pozici již nevlezou 2 kg hlíny, metoda vyhodí libovolnou výjimku.
    # - Pokud by po přidání hlíny celková hmotnost hlíny ve všech květináčích na pásu přesáhla celkovou
    #   maximální zátěž pásu, metoda vyhodí libovolnou výjimku.
    belt.add_soil("soft", 2)

    belt.add_soil("hard", 1)
    belt.add_soil("soft", 1)

    # Získá informace o obsahu hlínu v květináči na současné pozici.
    # - Pokud na současné pozici není květináč, vrátí metoda None.
    # - Pokud na současné pozici je květináč, vrátí n-tici se všemi typy hlín v květináči, spolu s
    #   celkovou váhou každého typu hlíny. Navrácená n-tice bude seřazená vzestupně dle názvu typu hlíny.
    soil = belt.get_pot()
    assert soil == (("hard", 1), ("soft", 3))

    # Odstraní květináč ze současné pozice.
    # - Pokud na současné pozici není květináč, metoda vyhodí libovolnou výjimku.
    # - Pokud květináč na současné pozici není zaplněn hlínou alespoň z poloviny své maximální hmotnosti,
    #   metoda vyhodí libovolnou výjimku.
    belt.take_pot()

    # Nastaví současnou pozici na pásu o jednu pozici doprava.
    belt.move_right()

    # Nastaví současnou pozici na pásu o jednu pozici doleva.
    belt.move_left()
    ```

    Další ukázky a okrajové situace naleznete v souboru `tests.py`.
    """
