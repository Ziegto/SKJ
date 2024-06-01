import pytest

from tasks import TaxEvaluator, TradeException, TransactionException, generate_wallet_info


def test_missing_person():
    evaluator = TaxEvaluator(["a"])
    with pytest.raises(TradeException):
        evaluator.buy_crypto("b", "Bitcoin", 750000, 1)


def test_total_coin_value():
    evaluator = TaxEvaluator(["a", "b"])
    evaluator.buy_crypto("a", "PyCoin", 8, 3)
    evaluator.buy_crypto("a", "PyCoin", 12, 2)
    evaluator.buy_crypto("a", "Bitcoin", 854233, 2)
    evaluator.sell_crypto("a", "Bitcoin", 923144, 1)

    evaluator.buy_crypto("b", "Bitcoin", 923003, 4)

    assert evaluator.total_coin_value("a", "PyCoin", 40) == 200
    assert evaluator.total_coin_value("a", "Bitcoin", 800000) == 800000
    assert evaluator.total_coin_value("b", "Bitcoin", 820000) == 3280000


def test_total_coin_value_unknown_empty_balance():
    evaluator = TaxEvaluator(["a"])
    assert evaluator.total_coin_value("a", "PyCoin", 8) == 0


def test_sell_profit():
    evaluator = TaxEvaluator(["a"])
    evaluator.buy_crypto("a", "PyCoin", 5, 3)
    evaluator.buy_crypto("a", "PyCoin", 10, 2)
    assert evaluator.sell_crypto("a", "PyCoin", 7, 4) == 3
    assert evaluator.sell_crypto("a", "PyCoin", 8, 1) == -2


def test_not_enough_coins_1():
    evaluator = TaxEvaluator(["a"])
    with pytest.raises(TradeException):
        assert evaluator.sell_crypto("a", "PyCoin", 1, 1)


def test_not_enough_coins_2():
    evaluator = TaxEvaluator(["a"])
    evaluator.buy_crypto("a", "PyCoin", 5, 2)
    evaluator.sell_crypto("a", "PyCoin", 5, 1)
    with pytest.raises(TradeException):
        assert evaluator.sell_crypto("a", "PyCoin", 5, 2)


def test_empty_tax():
    evaluator = TaxEvaluator(["a"])
    assert evaluator.get_tax("a") == 0


def test_negative_tax():
    evaluator = TaxEvaluator(["a"])
    evaluator.buy_crypto("a", "PyCoin", 5, 2)
    evaluator.sell_crypto("a", "PyCoin", 3, 2)
    assert evaluator.get_tax("a") == 0


def test_positive_tax():
    evaluator = TaxEvaluator(["a", "b"])
    evaluator.buy_crypto("a", "PyCoin", 5, 1)
    evaluator.sell_crypto("a", "PyCoin", 50, 1)
    assert evaluator.get_tax("a") == 7


def test_unrealized_gain_tax():
    evaluator = TaxEvaluator(["a", "b"])
    evaluator.buy_crypto("a", "PyCoin", 5, 1)
    evaluator.sell_crypto("a", "PyCoin", 50, 1)
    evaluator.buy_crypto("a", "Ethereum", 44376, 2)
    assert evaluator.get_tax("a") == 7


def test_rug_pull():
    evaluator = TaxEvaluator(["a", "b"])
    evaluator.buy_crypto("a", "Ethereum", 60231, 10)
    assert evaluator.sell_crypto("a", "Ethereum", 75892, 10) == 156610
    evaluator.buy_crypto("a", "PyCoin", 52, 100)
    assert evaluator.sell_crypto("a", "PyCoin", 522, 40) == 18800
    assert evaluator.sell_crypto("a", "PyCoin", 10102, 60) == 603000

    evaluator.buy_crypto("b", "PyCoin", 44, 5)
    evaluator.buy_crypto("b", "PyCoin", 54, 5)
    evaluator.buy_crypto("b", "PyCoin", 68, 5)
    evaluator.buy_crypto("b", "PyCoin", 203, 5)
    evaluator.buy_crypto("b", "PyCoin", 522, 5)
    evaluator.buy_crypto("b", "PyCoin", 10104, 5)
    evaluator.buy_crypto("b", "PyCoin", 400, 5)
    evaluator.buy_crypto("b", "PyCoin", 20, 5)
    evaluator.buy_crypto("b", "PyCoin", 4, 5)

    assert evaluator.sell_crypto("b", "PyCoin", 2, 45) == -57005

    assert evaluator.get_tax("a") == 116762
    assert evaluator.get_tax("b") == 0


def test_invalid_transaction_1():
    with pytest.raises(TransactionException):
        generate_wallet_info("tx-invalid-1.txt")


def test_invalid_transaction_2():
    with pytest.raises(TransactionException):
        generate_wallet_info("tx-invalid-2.txt")


def test_simple():
    assert generate_wallet_info("tx-simple.txt") == [{
        "balance": 20,
        "id": "ab",
        "incoming-count": 3,
        "most-frequent-target": "cd",
        "outgoing-count": 3
    }, {
        "balance": 680,
        "id": "cd",
        "incoming-count": 2,
        "most-frequent-target": "ce",
        "outgoing-count": 1
    }, {
        "balance": 150,
        "id": "ce",
        "incoming-count": 2,
        "most-frequent-target": "ab",
        "outgoing-count": 1
    }]


def test_no_outgoing():
    assert generate_wallet_info("tx-no-outgoing.txt") == [{
        "balance": 50,
        "id": "abx",
        "incoming-count": 1,
        "most-frequent-target": "bb",
        "outgoing-count": 1
    }, {
        "balance": 50,
        "id": "bb",
        "incoming-count": 1,
        "most-frequent-target": None,
        "outgoing-count": 0
    }]


def test_target_count_equal():
    assert generate_wallet_info("tx-target-count-equal.txt") == [{
        "balance": 120,
        "id": "abx",
        "incoming-count": 2,
        "most-frequent-target": "cxyz",
        "outgoing-count": 4
    }, {
        "balance": 120,
        "id": "cxyz",
        "incoming-count": 2,
        "most-frequent-target": "zz",
        "outgoing-count": 1
    }, {
        "balance": 110,
        "id": "zz",
        "incoming-count": 3,
        "most-frequent-target": "abx",
        "outgoing-count": 1
    }]


def test_self():
    assert generate_wallet_info("tx-self.txt") == [{
        "balance": 10,
        "id": "ab",
        "incoming-count": 2,
        "most-frequent-target": "ab",
        "outgoing-count": 1
    }]
