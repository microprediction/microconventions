import muid, time
from muid.mining import mine_once

class KeyConventions():
    """ Conventions for write_keys, which are Memorable Unique Identifiers (MUIDs)  See www.muid.org for more information """

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def is_valid_key(key):
        """ Check if key is hash-memorable """
        return isinstance(key,str) and muid.validate(key)

    @staticmethod
    def create_key(difficulty=6):
        """ Create new write_key (string, not bytes) """
        return muid.create(difficulty=difficulty).decode()

    @staticmethod
    def animal_from_key(key):
        return muid.animal(key)

    @staticmethod
    def key_difficulty(key):
        return len(muid.animal(key).replace(' ',''))

    @staticmethod
    def shash(key):
        """ Uses SHA-256 hash to create public identity from private key"""
        # Expects a string not binary
        return muid.shash(key)

    @staticmethod
    def animal_from_code(code):
        """ Return spirit animal given public identity (hash of write_key) """
        return muid.search(code=code)

    @staticmethod
    def maybe_create_key(seconds=1,difficulty=12):
        """ Find a write_key, perhaps
             :param difficulty:  int  minimum length of the memorable part of the hash
             :returns  str or None
        """
        quota = 100000000
        count = 0
        start_time = time.time()
        dffclty = difficulty
        while time.time()-start_time<seconds:
            report, dffclty, count = mine_once(dffclty, count, quota)
            if report:
                return report[0]["key"].decode()


new_key          = KeyConventions.create_key
create_key       = KeyConventions.create_key
maybe_create_key = KeyConventions.maybe_create_key
animal_from_key  = KeyConventions.animal_from_key
shash            = KeyConventions.shash
animal_from_code = KeyConventions.animal_from_code
key_difficulty   = KeyConventions.key_difficulty