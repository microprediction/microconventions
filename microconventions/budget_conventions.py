from microconventions.key_conventions import KeyConventions
from microconventions.type_conventions import Activity

# Conventions regarding stream budgets and bankruptcy


class BudgetConventions(KeyConventions):

    def __init__(self, min_difficulty, min_balance, **kwargs):
        self.MIN_BALANCE = min_balance
        self.min_balance = min_balance  # Backward compat
        self.MIN_DIFFICULTIES = {Activity.set:min_difficulty,
                                 Activity.mset:min_difficulty,
                                 Activity.submit: min_difficulty - 4,
                                 Activity.cset: min_difficulty + 1,
                                 Activity.give: min_difficulty-1,
                                 Activity.receive: min_difficulty-2}
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

    def permitted(self, activity:Activity, difficulty:int=None, write_key=None) ->bool:
        """ Determine ability to do stuff, or someone else's """
        difficulty = difficulty or self.difficulty(write_key=write_key)
        return difficulty >= self.MIN_DIFFICULTIES[activity]

    def permitted_to_set(self, difficulty:int=None, write_key=None):
        """ Determine whether you or someone else has permission to create stream """
        return self.permitted(activity=Activity.set, difficulty=difficulty, write_key=write_key)

    def permitted_to_submit(self, difficulty: int = None, write_key=None):
        """ Determine whether you or someone else has permission to create (update) stream """
        return self.permitted(activity=Activity.submit, difficulty=difficulty, write_key=write_key)

    def permitted_to_mset(self, difficulty: int = None, write_key=None):
        """ Determine whether you or someone else has permission to create (update) multiple streams  """
        return self.permitted(activity=Activity.mset, difficulty=difficulty, write_key=write_key)

    def permitted_to_cset(self, difficulty: int = None, write_key=None):
        """ Determine whether you or someone else has permission to create (update) multiple streams with implied Copulas  """
        return self.permitted(activity=Activity.mset, difficulty=difficulty, write_key=write_key)

    def permitted_to_give(self, difficulty: int = None, write_key=None ):
        """ Determine whether you or someone else has permission to transfer some of your balance """
        return self.permitted(activity=Activity.give, difficulty=difficulty, write_key=write_key)

    def permitted_to_receive(self, difficulty: int=None, write_key=None):
        """ Determine whether you or someone else has permission to receive some balance """
        return self.permitted(activity=Activity.receive, difficulty=difficulty, write_key=write_key)

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

    def maximum_stream_budget(self, difficulty:int=None, write_key:str=None) -> float:
        """ Default, and also maximum budget for yourself or someone else """
        difficulty = difficulty or self.difficulty(write_key=write_key)
        budget_1_difficulty = self.MIN_DIFFICULTIES[Activity.mset]
        return abs(self.bankruptcy_level(difficulty=difficulty) / self.bankruptcy_level(difficulty=budget_1_difficulty))