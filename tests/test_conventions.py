from microconventions.conventions import MicroConventions
from pprint import pprint


def test_constructor():
    mc = MicroConventions()
    for mandatory in ['min_balance', 'MIN_DIFFICULTIES', 'DELAYS','num_predictions']:
        assert mandatory in mc.__dict__


def test_stream_conventions():
    mc = MicroConventions()
    assert mc.is_valid_name('barney.json')
    assert not mc.is_valid_name('jeff%.json')
    assert mc.is_plain_name('jeff.json')
    assert not mc.is_plain_name('jeff~80.json')
    assert not mc.is_plain_name('jeff::70.json')
    assert 'json' in mc.random_name()
    assert '70' in mc.horizon_name(name='jeff.json', delay=70)
    assert 70 == mc.split_horizon_name('70::jeff.json')[1]
    assert mc.sep() == '::'


def test_horizon_conventions():
    mc = MicroConventions()
    assert len(mc.DELAYS) == 4
    assert all(isinstance(d, int) for d in mc.DELAYS)
    assert 'jeff' in mc.horizon_name(name='jeff.json', delay=70)


def test_key_conventions():
    mc = MicroConventions()
    key = '239a9ed9918ff4daf36073c074dc8334'
    assert mc.is_valid_key(key)
    assert mc.animal_from_key(key) == "Bee Camel"
    assert mc.shash(key) == "beeca3e13af4a0f2a0b484f5e8386c79"
    assert mc.animal_from_code("beeca3e13af4a0f2a0b484f5e8386c79") == "Bee Camel"
    assert len(mc.animal_from_key(mc.create_key(difficulty=6))) >= 6
    assert mc.maybe_create_key(seconds=0.1, difficulty=12) is None


def test_keys_imported():
    mc = MicroConventions()
    from microconventions import new_key, create_key, maybe_create_key, animal_from_key, key_difficulty, \
        animal_from_code
    assert maybe_create_key(seconds=0.1, difficulty=12) is None
    assert len(mc.animal_from_key(mc.create_key(difficulty=6))) >= 6
    assert len(animal_from_key(create_key(difficulty=6))) >= 6
    assert key_difficulty(create_key(difficulty=6)) >= 6
