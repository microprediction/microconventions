from microconventions.horizon_conventions import HorizonConventions
from microconventions import MicroConventions


def test_horizon_names():
    questions = [{'name': 'z1~cop.json', 'delay': 70} ]
    answers = [ '70::z1~cop.json'  ]
    hc = HorizonConventions(delays=[70,310,910,3555])
    for q, a in zip(questions, answers):
        a1 = HorizonConventions.horizon_name(**q)
        a2 = hc.horizon_name(**q)
        assert a1 == a
        assert a2 == a

def test_delays():
    mc = MicroConventions()
    assert len(mc.DELAYS)==4