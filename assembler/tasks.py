from typing import Tuple
import re


class ProgramException(BaseException):
    pass


# noinspection SpellCheckingInspection
def check_copilot(program: str) -> Tuple[str, int]:
    """
    Úkol 1

    Studenti předmětu APPS se pokoušejí použít službu Copilot pro vygenerování řešení zadaných
    úloh v x86 assembly, aby nemuseli přemýšlet. Bohužel se ale ukázalo, že AI občas generuje
    kód, který není správně naformátován, nebo přímo obsahuje nesmyslné instrukce.
    Pomozte nebohým studentům naimplementováním funkce `check_copilot`, která obdrží vygenerovaný
    program, opraví v něm formátování, chybné názvy instrukcí a zduplikované instrukce, a poté
    pro jistotu i program vykoná a zjistí jeho výsledek, aby šlo ověřit, že byl program vygenerován
    korektně.

    Funkce by měla vrátit dvojici hodnot. První hodnotou bude zformátovaný a opravený program,
    a druhou hodnotou bude obsah registru R0 po provedení opraveného programu.

    Assembly programy se skládají z řádků, řádek může být buď prázdný nebo může obsahovat jednu
    instrukci. Každá validní instrukce se skládá z opcodu a dvou výrazů:
    `<OPCODE> <ARG0> <ARG1>`

    Například:
    `MOV R0 5`

    <OPCODE> může být buď `MOV` nebo `ADD`.
    Výraz (argument) může být:
    - Konstanta: celé číslo
        - Hodnota tohoto výrazu odpovídá zadané konstantě.
    - Registr: `R<int>`, kde `<int>` je celé číslo v rozsahu 0 až 15.
        - Hodnota tohoto výrazu odpovídá současné hodnotě registru s daným indexem.
    - Index: `[<int>]` nebo `[R<int>]`.
        - Hodnota tohoto výrazu odpovídá současné hodnotě paměti na adrese dané hodnotou výrazu v
        hranatých závorkách.

    Pravidla formátování:
    - V řádku s instrukcí může být libovolné množství mezer. Při formátování znormalizujte
    instrukci tak, aby na začátku ani konci řádku mezery nebyly, a aby mezi třemi členy instrukce
    byla právě jedna mezera.
    `    MOV        R0  5    ` -> `MOV R0 5`
    - Ve vstupu se mohou vyskytnout prázdné řádky. Ty při formátování odstraňte.
    - Opcode může být vygenerovaný s chybou. opcode s chybou je definován tak, že má tři znaky,
    a liší se právě v jednom znaku od jedné ze známých instrukcí (MOV/ADD). Pokud naleznete opcode
    s chybou, tak jej opravte.
    `MXV R0 5` -> `MOV R0 5`
    `ADZ R0 5` -> `ADD R0 5`
    - Pokud se po zformátování ve vstupu vyskytnou stejné řádky za sebou, tak tyto duplicity vyraďte
    z výstupu.
    ```
    ADD R0 5
    ADX R0 5
    ADZ R0 5

    vvv

    ADD R0 5
    ```
    - Pokud bude ve vstupu jakýkoliv jiný obsah (chybějící argument, argumentů je moc, opcode nemá
    tři znaky nebo je moc vzdálen od známých instrukcí atd.), tak vyvolejte `ProgramException`.

    Jakmile bude program zformátován a opraven, tak jej vykonejte. Vytvořte si paměť (1000 čísel
    indexovaných od nuly) a registry (16 čísel indexovaných od nuly) a inicializujte vše na nulu.

    Poté vykonejte všechny instrukce, jednu po druhé.
    - Instrukce MOV <A> <B> načte hodnotu výrazu <B> a uloží jej do <A>.
    - Instrukce ADD <A> <B> načte hodnotu výrazu <B> a přičte jej k hodnotě umístění v <A>.

    V obou případech může <A> být buď registr nebo místo v paměti. Při pokusu o uložení do konstanty
    vyvolejte `ProgramException`.

    Příklad:
    ```
    MOV R0 5     # Ulož hodnotu 5 do registru R0
    ADD R0 1     # Přičti k registru R0 hodnotu 1 (v registru R0 poté bude hodnota 6)
    MOV R1 R0    # Ulož hodnotu registru R0 (6) do registru R1
    MOV [5] 8    # Ulož hodnotu 8 do paměti na adrese 5
    MOV [6] R0   # Ulož hodnotu registru R0 (6) do paměti na adrese 6
    MOV [R0] 5   # Ulož hodnotu 5 do paměti na adrese dané hodnotou registru R0 (6)
    MOV R1 [R0]  # Ulož hodnotu paměti na adrese dané hodnotou registru R0 (6) do registru R1
    ADD R0 R1    # Přičti k registru R0 hodnotu registru R1 (5)
    ```
    Po provedení tohoto programu by v registru R0 měla být hodnota 11.

    Po vykonání programu vraťte n-tici `(opravený a zformátovaný program, hodnota registru R0)`.
    """

    memory = [0] * 1000
    regs = [0] * 16

    # Helper function to clean and validate an opcode
    def clean_opcode(opcode):
        corrections = {"MOV": ["MO.", "M.V", ".OV"], "ADD": ["AD.", "A.D", ".DD"]}
        for correct_opcode, patterns in corrections.items():
            if any(re.match(pattern, opcode) for pattern in patterns):
                return correct_opcode
        if opcode not in ["MOV", "ADD"]:
            raise ProgramException()
        return opcode

    # Helper function to parse and validate arguments
    def parse_arg(arg):
        if arg.startswith("[") and arg.endswith("]"):
            inner_arg = arg[1:-1]
            if inner_arg.isdigit():
                addr = int(inner_arg)
                if 0 <= addr < 1000:
                    return ("mem", addr)
            elif inner_arg.startswith("R") and inner_arg[1:].isdigit():
                reg = int(inner_arg[1:])
                if 0 <= reg < 16:
                    return ("mem_reg", reg)
        elif arg.isdigit():
            return ("const", int(arg))
        elif arg.startswith("R") and arg[1:].isdigit():
            reg = int(arg[1:])
            if 0 <= reg < 16:
                return ("reg", reg)
        raise ProgramException()

    # Parse and clean the program
    lines = program.strip().split("\n")
    cleaned_program = []
    for line in lines:
        line = " ".join(line.split())
        if not line:
            continue
        parts = line.split()
        if len(parts) != 3:
            raise ProgramException()
        opcode, arg1, arg2 = parts
        opcode = clean_opcode(opcode)
        cleaned_program.append(f"{opcode} {arg1} {arg2}")

    # Remove duplicate consecutive instructions
    deduped_program = []
    for i in range(len(cleaned_program)):
        if i == 0 or cleaned_program[i] != cleaned_program[i - 1]:
            deduped_program.append(cleaned_program[i])

    # Execute the cleaned program
    for line in deduped_program:
        parts = line.split()
        opcode, arg1, arg2 = parts
        type1, value1 = parse_arg(arg1)
        type2, value2 = parse_arg(arg2)

        if type1 == "const":
            raise ProgramException()

        if type2 == "const":
            value2 = value2
        elif type2 == "reg":
            value2 = regs[value2]
        elif type2 == "mem":
            value2 = memory[value2]
        elif type2 == "mem_reg":
            value2 = memory[regs[value2]]

        if opcode == "MOV":
            if type1 == "reg":
                regs[value1] = value2
            elif type1 == "mem":
                memory[value1] = value2
            elif type1 == "mem_reg":
                memory[regs[value1]] = value2
        elif opcode == "ADD":
            if type1 == "reg":
                regs[value1] += value2
            elif type1 == "mem":
                memory[value1] += value2
            elif type1 == "mem_reg":
                memory[regs[value1]] += value2

    return "\n".join(deduped_program) + "\n", regs[0]


"""
Úkol 2

Zkrácený semestr, spousta projektů a domácích úloh stresuje studenty! Někteří učitelé nedávají
feedback na úlohy, zapisují jej do různých systémů (Edison, Kelvin, Excel) a studenti pak neví,
na čem jsou. Pomozte jim tím, že naimplementujete třídu `StudyDatabase`, která bude uchovávat
informace o získaných bodech studenta v jednotlivých předmětech a typech úloh
("lesson", "project", "test").

Třída bude poskytovat následující rozhraní:
```python
# Vytvoření databáze
db = StudyDatabase()

# Metoda `add_points` zaznamená jednotlivé získané body pro daný předmět a typ úlohy
# ("project", "lesson", "test"). Zároveň vrátí celkový počet bodů pro daný předmět a typ úlohy
# (včetně nově přidaných bodů).
db.add_points("SKJ", "lesson", 5)    # 5
db.add_points("SKJ", "lesson", 10)   # 15

# Metoda `total_points_per_subject` vrátí slovník s celkovým počtem bodů pro každý
# zaznamenaný předmět.
db.total_points_per_subject()        # {"SKJ": 15}

db.add_points("SKJ", "test", 40)     # 40
db.add_points("UTI", "lesson", 10)   # 10

# Této metodě můžeme předat typ úlohy. V tom případě vrátí pouze body tohoto typu úlohy.
db.total_points_per_subject("lesson") # {"SKJ": 15, "UTI": 10}
db.total_points_per_subject()         # {"SKJ": 55, "UTI": 10}

# Metoda `average_points_per_type` vrátí průměrný počet bodů pro daný typ úlohy pro jednotlivé
# předměty. Průměr zaokrouhlete dolů (směrem k nule) na celé číslo.
db.average_points_per_type("lesson")  # {"SKJ": 7, "UTI": 10}

db.add_points("C++ I", "project", 40) # 40
db.add_points("C++ I", "lesson", 60)  # 60

# Metoda `passed_subjects` vrátí seznam předmětů, ze kterých student již získal dohromady
# alespoň 51 bodů. Seznam navrácených předmětů seřaďte vzestupně dle jejich jména.
db.passed_subjects()                  # ["C++ I", "SKJ"]
```
"""


class StudyDatabase:

    def __init__(self):
        self.subjects = {}
        self.count = {}

    def add_points(self, subject, tyype, points):
        if subject not in self.subjects:
            self.subjects[subject] = {}
            self.count[subject] = {}
        if tyype not in self.subjects[subject]:
            self.subjects[subject][tyype] = 0
            self.count[subject][tyype] = 0
        self.subjects[subject][tyype] += points
        self.count[subject][tyype] += 1
        return self.subjects[subject][tyype]

    def total_points_per_subject(self, tyype=None):
        if tyype is None:
            return {subject: sum(self.subjects[subject].values()) for subject in self.subjects}
        else:
            for subject in self.subjects:
                if tyype not in self.subjects[subject]:
                    self.subjects[subject][tyype] = 0
            return {subject: self.subjects[subject][tyype] for subject in self.subjects}

    def passed_subjects(self):
        passed = [subject for subject in self.subjects if sum(self.subjects[subject].values()) >= 51]
        return sorted(passed)

    def average_points_per_type(self, target):
        out = {}

        for subject in self.subjects:
            out[subject] = 0

            if target not in self.subjects[subject]:
                continue
            else:
                for tyype in self.subjects[subject]:
                    if tyype == target:
                        out[subject] += self.subjects[subject][tyype]

                out[subject] //= self.count[subject][target]

        return out
