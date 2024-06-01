from typing import Tuple

import pytest

from tasks import find_dangerous_contacts, VaccinationCenter


def test_find_dangerous_contacts_distance_1():
    contacts = find_dangerous_contacts("test1.txt", 1.0)
    assert contacts == []


def test_find_dangerous_contacts_distance_2():
    contacts = find_dangerous_contacts("test1.txt", 2.0)
    assert contacts == [('Anna', 'Jana')]


def test_find_dangerous_contacts_distance_5():
    contacts = find_dangerous_contacts("test1.txt", 5.0)
    assert contacts == [('Anna', 'Jana'),
                        ('František', 'Karel'),
                        ('František', 'Lenka'),
                        ('Jana', 'Lukáš'),
                        ('Jana', 'Martin'),
                        ('Lukáš', 'Martin')]


def test_vaccination_center_blocked_vaccination_room():
    c = VaccinationCenter(3, 3)
    c.accept_patient(1)
    c.accept_patient(1)
    c.accept_patient(1)

    # no more room left in vaccination room
    with pytest.raises(Exception):
        c.accept_patient(1)
    c.advance_time(3)
    c.accept_patient(1)


def test_vaccination_center_blocked_waiting_room():
    c = VaccinationCenter(3, 1)
    assert get_stats(c) == (0, 0, 0)
    c.accept_patient(10)
    assert get_stats(c) == (1, 0, 0)

    c.accept_patient(10)
    assert get_stats(c) == (2, 0, 0)

    # vaccinate both users
    c.advance_time(3)

    # one of the users will be stuck
    assert get_stats(c) == (1, 1, 0)
    c.advance_time(1)
    assert get_stats(c) == (1, 1, 0)
    c.advance_time(9)
    assert get_stats(c) == (0, 1, 1)
    c.advance_time(9)
    assert get_stats(c) == (0, 1, 1)
    c.advance_time(1)
    assert get_stats(c) == (0, 0, 2)


def test_vaccination_center_move_two_at_once():
    c = VaccinationCenter(3, 2)
    assert get_stats(c) == (0, 0, 0)
    c.accept_patient(10)
    assert get_stats(c) == (1, 0, 0)

    c.accept_patient(10)
    assert get_stats(c) == (2, 0, 0)

    # vaccinate both users
    c.advance_time(3)

    # both users should be moved
    assert get_stats(c) == (0, 2, 0)
    c.advance_time(10)
    assert get_stats(c) == (0, 0, 2)


def test_vaccination_center_keep_patient_order_1():
    c = VaccinationCenter(3, 1)
    assert get_stats(c) == (0, 0, 0)
    c.accept_patient(10)
    assert get_stats(c) == (1, 0, 0)

    # second patient has short wait time, but he will not be preferred
    c.accept_patient(1)
    assert get_stats(c) == (2, 0, 0)

    # vaccinate both users
    c.advance_time(3)

    # one of the users will be stuck
    assert get_stats(c) == (1, 1, 0)
    c.advance_time(1)
    assert get_stats(c) == (1, 1, 0)
    c.advance_time(9)
    assert get_stats(c) == (0, 1, 1)
    c.advance_time(1)
    assert get_stats(c) == (0, 0, 2)


def test_vaccination_center_keep_patient_order_2():
    c = VaccinationCenter(3, 1)
    assert get_stats(c) == (0, 0, 0)
    c.accept_patient(1)
    assert get_stats(c) == (1, 0, 0)

    # second patient has short wait time, but he will not be preferred
    c.accept_patient(10)
    assert get_stats(c) == (2, 0, 0)

    # vaccinate both users
    c.advance_time(3)

    # one of the users will be stuck
    assert get_stats(c) == (1, 1, 0)
    c.advance_time(1)
    assert get_stats(c) == (0, 1, 1)
    c.advance_time(9)
    assert get_stats(c) == (0, 1, 1)
    c.advance_time(10)
    assert get_stats(c) == (0, 0, 2)


def test_vaccination_center_move_atomically():
    c = VaccinationCenter(3, 2)
    assert get_stats(c) == (0, 0, 0)
    c.accept_patient(1)
    c.accept_patient(1)
    assert get_stats(c) == (2, 0, 0)

    # vaccinate both users
    c.advance_time(1)
    assert get_stats(c) == (2, 0, 0)
    c.accept_patient(3)
    assert get_stats(c) == (3, 0, 0)
    c.advance_time(3)
    assert get_stats(c) == (0, 1, 2)
    c.advance_time(3)
    assert get_stats(c) == (0, 0, 3)


def get_stats(center: VaccinationCenter) -> Tuple[int, int, int]:
    return (center.vaccination_room_count(), center.waiting_room_count(), center.patient_finished_count())
