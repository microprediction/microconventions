from microconventions.budget_conventions import BudgetConventions
from microconventions.key_conventions import KeyConventions


BUDGET_KWARGS = {'min_len':10,'min_balance':-1}


class Kid(BudgetConventions):

    def __init__(self):
        super().__init__(**BUDGET_KWARGS)
        self.write_key = KeyConventions.create_key(difficulty=8)


class BigKid(Kid):

    def __init__(self):
        super().__init__()

    def get_balance(self,write_key=None):
        return 17.3


def test_kid():
    kid = Kid()
    assert kid.difficulty() >= 8
    assert kid.difficulty(write_key=kid.write_key) >= 8
    assert kid.bankruptcy_level()<0
    assert kid.bankruptcy_level(difficulty=8) < 0
    assert kid.bankruptcy_level(difficulty=12) < -10
    assert kid.bankruptcy_level(write_key=kid.write_key) <0
    assert kid.distance_to_bankruptcy(balance=-1, level=-10) > 0
    assert kid.distance_to_bankruptcy(balance=10) > 10



def test_bigkid():
    big = BigKid()
    assert not big.bankrupt()
    assert big.distance_to_bankruptcy()>10


def test__is_valid_key():
    bc = BudgetConventions(**BUDGET_KWARGS)
    s = bc.create_key(difficulty=6)
    assert bc.is_valid_key(s), "Thought  " + s + " should be valid."
    assert bc.is_valid_key("too short") == False, "Thought  " + s + " should be invalid"


def test_difficulty():
    bc = BudgetConventions(**BUDGET_KWARGS)
    assert bc.key_difficulty('not a key')==0
    s = bc.create_key(difficulty=6)
    assert bc.key_difficulty(s)>=6




