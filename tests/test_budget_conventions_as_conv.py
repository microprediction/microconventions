from microconventions.conventions import MicroConventions
from microconventions.type_conventions import Activity
from microconventions.key_conventions import create_key


KWARGS = {'min_len':10, 'min_balance':-1, 'delays':[1, 2, 3],'num_predictions':52}


class MicroKid(MicroConventions):

    def __init__(self):
        super().__init__(**KWARGS)
        self.write_key = create_key(difficulty=8)


class BigKid(MicroKid):

    def __init__(self):
        super().__init__()

    def get_balance(self,write_key=None):
        return 17.3


def test_kid():
    kid = MicroKid()
    assert kid.difficulty() >= 8
    assert kid.difficulty(write_key=kid.write_key) >= 8
    assert not kid.permitted_to_cset()
    assert not kid.permitted_to_mset()
    assert not kid.permitted_to_set()
    assert kid.permitted_to_submit()
    assert kid.bankruptcy_level()<0
    assert kid.bankruptcy_level(difficulty=8) < 0
    assert kid.bankruptcy_level(difficulty=12) < -10
    assert kid.bankruptcy_level(write_key=kid.write_key) <0
    assert kid.distance_to_bankruptcy(balance=-1, level=-10) > 0
    assert kid.distance_to_bankruptcy(balance=10) > 10
    assert kid.maximum_stream_budget()<0.1


def test_bigkid():
    big = BigKid()
    assert not big.bankrupt()
    assert big.distance_to_bankruptcy()>10



