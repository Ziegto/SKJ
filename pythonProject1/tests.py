import pytest

from tasks import spocti_krychli, OvladaciPanel, nejcastejsi_glyfy, nejvetsi_poklad, analyzuj_logy, je_palindrom, Knihovna


def test_knihovna():
    knihovna = Knihovna()
    knihovna.pridej_knihu("Harry Potter")
    knihovna.pridej_knihu("Harry Potter")
    knihovna.pridej_knihu("Lord of the Rings")
    knihovna.pridej_knihu("Artemis Fowl")
    assert knihovna.vypujc_knihu("Lord of the Rings") == True
    assert knihovna.vrat_pocet_kopii() == 3
    assert knihovna.vrat_nejcetnejsi_knihu() == "Harry Potter"


def test_spocti_krychli():
    assert spocti_krychli("souradnice.txt") == 255013440


def test_ovladaci_panel():
    panel = OvladaciPanel(["A", "B", "C"])
    panel.posun_doprava()
    panel.zadej_znak()
    panel.posun_doprava()
    panel.posun_doprava()
    panel.zadej_znak()
    panel.posun_doleva()
    panel.zadej_znak()
    assert panel.vytoc_adresu() == ["B", "A", "C"]


def test_nejcastejsi_glyfy():
    assert nejcastejsi_glyfy("planety.txt") == [
        ('Sagittarius', 51), ('Hydra', 39), ('Libra', 38),
        ('Perseus', 38), ('Aries', 37), ('Capricornus', 37),
        ('Virgo', 37), ('Auriga', 36), ('Crater', 36),
        ('Eridanus', 36), ('Lynx', 36), ('Scorpius', 36),
        ('Norma', 34), ('Orion', 32), ('Scutum', 31),
        ('Sextans', 31), ('Centaurus', 30), ('Gemini', 30),
        ('Bootes', 29), ('Taurus', 26)
    ]


def test_nejvetsi_poklad():
    assert nejvetsi_poklad("artefakty.txt") == ('Kniha', 5)


def test_analyzuj_logy():
    assert analyzuj_logy("log.txt") == [
        (200, 2), (500, 1), (404, 1), (302, 1)
    ]


def test_je_palindrom():
    assert je_palindrom('')
    assert je_palindrom('a')
    assert je_palindrom('aa')
    assert je_palindrom('aaa')
    assert je_palindrom('aba')
    assert not je_palindrom('abc')
    assert not je_palindrom('abcd')
    assert not je_palindrom('palindrom')
