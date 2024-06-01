def find_dangerous_contacts(file: str, max_distance: float):
    """
    Úkol 1

    Server aplikace eRouška se pokazil a nelze tak vyhodnocovat rizikové kontakty!
    Pomozte situaci napravit tak, že naimplementujete funkci `find_dangerous_contacts`.

    Funkce obdrží cestu k textovému souboru v parametru `file` a maximální vzdálenost, která je
    ještě pokládána za rizikový kontakt, v parametru `max_distance`.

    V souboru budou záznamy o pozicích (X, Y, Z) jednotlivých uživatelů aplikace, spolu s časovým
    razítkem, kdy na dané pozici daný uživatel byl. V jeden čas může být jeden uživatel maximálně
    na jedné pozici.

    Každý záznam bude na samostatném řádku ve formátu `<časové razítko>: <uživatel> <x> <y> <z>`.
    Příklad souboru:
    ```
    3: karel 1 2 5
    2: jana 8 9 3
    0: martina -3 6 8
    2: františek 7 9 3
    3: františek 1 2 3
    ```

    První záznam říká, že v čase 3 byl karel na pozici (1, 2, 5), druhý záznam říká, že v čase 2
    byla jana na pozici (8, 9, 3) atd.

    Zpracujte záznamy a nalezněte mezi nimi všechny rizikové kontakty. Rizikový kontakt mezi
    uživatelem A a B je definován tak, že oba uživatelé byli ve stejném čase na pozicích, mezi nimiž
    byla vzdálenost maximálně `max_distance`. Pro výpočet vzdálenosti použijte klasickou Euklidovskou
    vzdálenost (https://cs.wikipedia.org/wiki/Eukleidovsk%C3%A1_metrika).

    Vlastnosti rizikovách kontaktů:
    - Každý rizikový kontakt reprezentujte dvojicí (uzivatel_a, uzivatel_b).
    Např. ("karel", "františek").
    - V každé dvojici rizikového kontaktu seřaďte uživatele podle jejich jména vzestupně.
    - Pokud k rizikovému kontaktu dojde vícekrát, další kontakty ignorujte.
    - Uživatel nemůže mít rizikový kontakt sám se sebou.
    - Rizikový kontakt mezi uživateli A/B a B/A se počítá jako ten stejný kontakt.

    Vraťte z funkce pole rizikových kontaktů seřazené dle jmén obou uživatelů vzestupně.
    Např.
    [
        ("anežka", "bára"),
        ("anežka", "karel"),
        ("bára", "karel")
    ]

    Ukázkové výstupy pro vstupní soubor `test1.txt` naleznete v souboru `tests.py`.
    """


class VaccinationCenter:
    """
    Úkol 2

    Očkovací centrum na Černé louce napadli hackeři a znemožnili tak fungování jejich systému.
    Vytvořte třídu `VaccinationCenter`, která bude simulovat chod očkovacího centra.

    Třída bude modelovat dvě místnosti: místnost, kde probíhá očkování, a místnost, kam jdou pacienti
    po očkování na pozorování. Každá místnost má omezenou kapacitu.
    Centrum si musí udržovat informaci o tom, kolik pacientů je v jaké místnosti, přesouvat je mezi
    místnostmi v průběhu simulace a umožňovat přichod nových pacientů.

    Simulace centra bude probíhat v diskrétních časových jednotkách (čas 1, čas 2, čas 3 atd.).

    Pravidla fungování centra:
    - Pacient nemůže být přijat, pokud není dostatečná kapacita v místnosti pro očkování.
    - Po přijetí bude pacient umístěn do místnosti očkování a začne proces očkování, který bude trvat
    vždy 3 časové jednotky.
    - Po uplynutí očkování jsou pacienti přesunuti do místnosti pro pozorování v pořadí, ve kterém
    byli přijati do centra. Přesunuti ale mohou být pouze, pokud je v druhé místnosti místo!
    Pokud v ní místo není, musí zůstat v místnosti pro očkování, než se místo uvolní.
    Může se stát, že v jednom časovém kroku se budou chtít přesunout např. dva pacienti, ale místo
    bude pouze pro jednoho. Toho druhého tak budete muset prozatím nechat v první místnosti.
    - Jakmile je místo v místnosti pro pozorování, pacient tam bude přesunut a vyčká tam dobu, která
    je specifická pro každého pacienta (bude nastavena při jeho přijetí).
    - Po uplynutí času čekání v místnosti pro pozorování pacient z centra odejde a uvolní v místnosti
    místo. V každém kroku simulace nejprve nechte odejít všechny pacienty, kteří už čekali dostatečně
    dlouho v druhé místnosti, a teprve poté začněte přesouvat naočkované pacienty z první místnosti
    do druhé.
    - Centrum bude umožňovat zjištění aktuálního počtu pacientů v obou místnostech a také počet
    pacientů, kteří již z centra odešli s dokončeným očkováním.

    Třída bude poskytovat následující rozhraní:

    ```python
    # Vytvoření centra s kapacitou místnosti pro očkování 3 a kapacitou místnosti pro pozorování 4
    center = VaccinationCenter(3, 4)

    # Získání počtu pacientů, kteří jsou zrovna v místnosti pro očkování
    center.vaccination_room_count()

    # Získání počtu pacientů, kteří jsou zrovna v místnosti pro pozorování
    center.waiting_room_count()

    # Získání počtu pacientů, kteří již zcela dokončili očkování a odešli z očkovacího centra
    center.patient_finished_count()

    # Přijetí nového pacienta, který bude v druhé místnosti pozorován po dobu `n` časových jednotek
    # Pokud v současné době není dostatek místa pro přijetí zákazníka, metoda vyhodí (libovolnou)
    # výjimku.
    center.accept_patient(n)

    # Posun času simulace centra o `n` časových jednotek
    center.advance_time(n)
    ```

    Další ukázky a modelové situace naleznete v souboru `tests.py`.
    """
    pass
