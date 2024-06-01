import pytest

from tasks import CounterManager, frequent_visitors


def test_frequent_visitors_empty():
    assert frequent_visitors("test2.txt") == (
        (0, 0, 0, 0, 0, 0, 0),
        ()
    )


def test_frequent_visitors_repeated_visit():
    assert frequent_visitors("test1.txt") == (
        (1, 0, 0, 0, 0, 0, 0),
        ((42, 1), )
    )


def test_frequent_visitors_wrap_week():
    assert frequent_visitors("test3.txt") == (
        ((9, 4, 5, 2, 3, 3, 1),
         ((2, 5),
          (1, 5),
          (33, 4),
          (9, 3),
          (8, 2),
          (5, 2),
          (3, 2),
          (34, 1),
          (7, 1),
          (6, 1),
          (4, 1)))
    )


def test_counter_manager_no_counters():
    counter_manager = CounterManager([])
    with pytest.raises(Exception):
        counter_manager.queue_visitor([])
    with pytest.raises(Exception):
        counter_manager.queue_visitor(["pas"])


def test_counter_manager_queue_no_counter():
    counter_manager = CounterManager([["pas", "občanka"], ["schránka"]])
    with pytest.raises(Exception):
        counter_manager.queue_visitor(["řidičák"])
    with pytest.raises(Exception):
        counter_manager.queue_visitor(["pas", "občanka", "schránka"])


def test_counter_manager_queue_smaller_id():
    counter_manager = CounterManager([["pas", "občanka"], ["schranka"], ["pas"]])
    assert counter_manager.queue_visitor(["pas"]) == 1
    assert counter_manager.queue_visitor(["pas", "občanka"]) == 1
    assert counter_manager.queue_visitor(["pas"]) == 3


def test_counter_manager_round_robin():
    counter_manager = CounterManager([["pas"], ["pas"]])
    assert counter_manager.queue_visitor(["pas"]) == 1
    assert counter_manager.queue_visitor(["pas"]) == 2
    assert counter_manager.queue_visitor(["pas"]) == 1
    assert counter_manager.queue_visitor(["pas"]) == 2
    assert counter_manager.queue_visitor(["pas"]) == 1
    assert counter_manager.queue_visitor(["pas"]) == 2


def test_counter_manager_no_requirements():
    counter_manager = CounterManager([[], ["pas"]])
    assert counter_manager.queue_visitor(["pas"]) == 2
    assert counter_manager.queue_visitor(["pas"]) == 2
    assert counter_manager.queue_visitor([]) == 1
    assert counter_manager.queue_visitor([]) == 1
    assert counter_manager.queue_visitor([]) == 1
    assert counter_manager.queue_visitor([]) == 2


def test_counter_manager_full_queue():
    counter_manager = CounterManager([["pas"]])
    for _ in range(5):
        counter_manager.queue_visitor(["pas"])
    assert counter_manager.counter_queue_sizes() == [5]
    with pytest.raises(Exception):
        counter_manager.queue_visitor(["pas"])


def test_counter_manager_advance_no_queue():
    counter_manager = CounterManager([["pas", "obcanka"], ["schranka"], ["pas"]])
    with pytest.raises(Exception):
        counter_manager.counter_advance(0)


def test_counter_manager_advance_wrong_counter_id():
    counter_manager = CounterManager([["pas", "obcanka"], ["schranka"], ["pas"]])
    with pytest.raises(Exception):
        counter_manager.counter_advance(-1)
    with pytest.raises(Exception):
        counter_manager.counter_advance(0)
    with pytest.raises(Exception):
        counter_manager.counter_advance(4)


def test_counter_manager_advance():
    counter_manager = CounterManager([["pas", "obcanka"], ["schranka"], ["pas", "ridicak"]])
    assert counter_manager.queue_visitor(["pas"]) == 1
    assert counter_manager.queue_visitor(["pas", "obcanka"]) == 1
    assert counter_manager.queue_visitor(["pas"]) == 3
    assert counter_manager.counter_queue_sizes() == [2, 0, 1]

    counter_manager.counter_advance(1)
    assert counter_manager.counter_queue_sizes() == [1, 0, 1]
    assert counter_manager.queue_visitor(["schranka"]) == 2
    assert counter_manager.queue_visitor(["pas", "ridicak"]) == 3
    assert counter_manager.counter_queue_sizes() == [1, 1, 2]

    counter_manager.counter_advance(2)
    counter_manager.counter_advance(3)
    assert counter_manager.counter_queue_sizes() == [1, 0, 1]

    counter_manager.counter_advance(1)
    counter_manager.counter_advance(3)
    assert counter_manager.counter_queue_sizes() == [0, 0, 0]


def test_counter_manager_finished():
    counter_manager = CounterManager([["pas", "obcanka"], ["schranka"], ["pas"]])
    counter_manager.queue_visitor(["pas"])
    counter_manager.queue_visitor(["pas"])
    counter_manager.queue_visitor(["schranka"])
    counter_manager.queue_visitor(["pas"])
    counter_manager.queue_visitor(["pas"])
    counter_manager.queue_visitor(["pas"])

    while any(counter_manager.counter_queue_sizes()):
        for (index, count) in enumerate(counter_manager.counter_queue_sizes()):
            if count:
                counter_manager.counter_advance(index + 1)
    assert counter_manager.counter_finished_visitors() == [3, 1, 2]
