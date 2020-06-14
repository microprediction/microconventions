
from microconventions.stream_conventions import StreamConventions


def test_is_valid_name():
    nc = StreamConventions()
    s = 'dog-7214.json'
    assert nc.is_valid_name(s), "oops"
    for s in ["25824ee3-d9bf-4923-9be7-19d6c2aafcee.json"]:
        assert nc.is_valid_name(s),"Got it wrong for "+s


def test_its_testing_tuesday_i_am_so_happy():
    okay_names = ['mystream.json','ice_cream.json','tilde~in_there.json']
    bad_names  = ['toomanycolons::.json','spec@lcharacter.json','forgotjson']
    for name in okay_names:
        assert StreamConventions.is_valid_name(name)
    for name in bad_names:
        assert not StreamConventions.is_valid_name(name)