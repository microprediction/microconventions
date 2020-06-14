
from microconventions.sep_conventions import SepConventions


def test_i_am_writing_tests_while_watching_ozark():
    conv = SepConventions()
    assert SepConventions.sep() == '::'
    assert conv.SEP == '::'
    assert SepConventions.tilde() == '~'
    assert conv.TILDE== '~'
