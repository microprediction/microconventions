from microconventions.key_conventions import KeyConventions


def test__is_valid_key():
    kc = KeyConventions()
    s = kc.create_key(difficulty=6)
    assert kc.is_valid_key(s), "Thought  " + s + " should be valid."
    assert kc.is_valid_key("too short") == False, "Thought  " + s + " should be invalid"
