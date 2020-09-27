from microconventions.key_conventions import KeyConventions

# Conventions regarding stream budgets and bankruptcy


class BudgetConventions(KeyConventions):

    def __init__(self, min_len, min_balance, **kwargs):
        self.MIN_BALANCE = min_balance
        self.min_balance = min_balance  # Backward compat
        self.min_len = min_len
        super().__init__(**kwargs)

    def _write_key(self):
        """ Retrieve write_key from descendant (e.g. MicroWriter), or raise """
        try:
            return self.write_key
        except AttributeError:
            raise ('Supply write_key')

    def _get_balance(self, write_key=None):
        """ Retrieve write_key from descendant (e.g. MicroWriter), or raise """
        write_key = write_key or self._write_key()
        try:
            return self.get_balance(write_key=write_key)
        except AttributeError:
            raise Exception('Supply write_key')

    def bankruptcy_level(self, difficulty:int=None, write_key:str=None):
        difficulty = difficulty or self.difficulty(write_key=write_key)
        if difficulty <= 8:
            return -0.001
        return -1.0 * (abs(self.MIN_BALANCE) * (16 ** (difficulty - 9)))

    def difficulty(self, write_key:str=None):
        """ Difficulty of your own key, or someone else's """
        write_key = write_key or self._write_key()
        return self.key_difficulty(write_key)

    def bankrupt(self, write_key:str=None) -> bool:
        """ Own bankruptcy indicator, or someone else's """
        write_key = write_key or self._write_key()
        return self.distance_to_bankruptcy(write_key=write_key) < 0

    def distance_to_bankruptcy(self, balance:float=None, level:float=None, write_key:str=None) -> float:
        """ Own distance to bankruptcy, or someone else's """
        balance = balance or self._get_balance(write_key=write_key)
        level = level or self.bankruptcy_level(write_key=write_key)
        return balance - level

