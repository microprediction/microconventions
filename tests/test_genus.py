from microconventions.type_conventions import Genus


def test_from():
    assert Genus.regular == Genus.from_name('bill.json')
    assert Genus.zscore == Genus.from_name('z1~bill.json')
    assert Genus.bivariate == Genus.from_name('z2~bill.json')
    assert Genus.trivariate == Genus.from_name('z3~bill.json')
