import muid, time
from muid.mining import mine_once


class KeyConventions():
    """ Conventions for write_keys, which are Memorable Unique Identifiers (MUIDs)  See www.muid.org for more information """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def is_valid_key(key):
        """ Check if key is hash-memorable """
        return isinstance(key, str) and muid.validate(key)

    @staticmethod
    def create_key(difficulty=8, exact=False):
        """ Create new write_key (string, not bytes)

                exact - Insist on supplied difficulty.
                        If exact is not set to True, the key might be higher difficulty than requested
        """
        assert difficulty<18, "Be realistic!"
        while True:
            write_key = muid.create(difficulty=difficulty).decode()
            if not exact:
                return write_key
            else:
                actual_difficulty = KeyConventions.key_difficulty(write_key=write_key)
                if difficulty==actual_difficulty:
                    return write_key


    @staticmethod
    def animal_from_key(write_key):
        return muid.animal(write_key)

    @staticmethod
    def key_difficulty(write_key):
        nml = muid.animal(write_key)
        return 0 if nml is None else len(nml.replace(' ',''))

    @staticmethod
    def shash(write_key):
        """ Uses SHA-256 hash to create public identity from private key"""
        # Expects a string not binary
        return muid.shash(write_key)

    @staticmethod
    def animal_from_code(code):
        """ Return spirit animal given public identity (hash of write_key) """
        return muid.search(code=code)

    @staticmethod
    def maybe_create_key(seconds=1, difficulty=11):
        """ Find a write_key, perhaps
             :param difficulty:  int  minimum length of the memorable part of the hash
             :returns  str or None
        """
        quota = 100000000
        count = 0
        start_time = time.time()
        dffclty = difficulty
        while time.time() - start_time < seconds:
            report, dffclty, count = mine_once(dffclty, count, quota)
            if report:
                return report[0]["key"].decode()

    def code_from_code_or_key(self, code_or_key):
        if self.is_valid_key(code_or_key):
            return self.shash(code_or_key)
        elif self.animal_from_code(code_or_key):
            return code_or_key


new_key = KeyConventions.create_key
create_key = KeyConventions.create_key
maybe_create_key = KeyConventions.maybe_create_key
animal_from_key = KeyConventions.animal_from_key
shash = KeyConventions.shash
animal_from_code = KeyConventions.animal_from_code
key_difficulty = KeyConventions.key_difficulty
code_from_code_or_key = KeyConventions.code_from_code_or_key