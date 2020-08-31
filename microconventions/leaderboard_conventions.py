from microconventions.sep_conventions import SepConventions
from enum import Enum
from microconventions.type_conventions import Genus


class LeaderboardVariety(Enum):
    """ Enumerates varieties of leaderboards """
    memory = 0
    delay = 1
    name = 2
    sponsor = 3
    genus = 4
    name_and_delay = 21
    sponsor_and_delay = 31
    sponsor_and_genus = 34

    def __str__(self):
        return super().__str__().split('.')[1]

    def split(self):
        return self.__str__().split('_and_')

    def instance_name(self, **kwargs):
        return SepConventions.pipe().join( [ str(kwargs[k]) for k in self.split() ])


class LeaderboardConventions(SepConventions):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LEADERBOARD = "leaderboard" + self.SEP
        self.CUSTOM_LEADERBOARD = 'custom_leaderboard' + self.SEP  # Deprecated
        self.MEMORY = 10000   # Default memory used for most streams
        self.MEMORIES = [1000,10000]
        self.NUMERIC_ATTRIBUTES = ['delay','memory']

    def leaderboard_name(self, leaderboard_variety:LeaderboardVariety, **kwargs):
        """ Name for leaderboards """
        return self.LEADERBOARD + str(leaderboard_variety) + self.SEP + leaderboard_variety.instance_name(**kwargs)

    def stream_leaderboard_names(self, name, sponsor, delay):
        genus = Genus.from_name(name=name)
        memory_boards = [ self.leaderboard_name(leaderboard_variety=LeaderboardVariety.memory,memory=memory) for memory in self.MEMORIES if not memory==self.MEMORY ]
        stream_boards  = [ self.leaderboard_name(leaderboard_variety=variety, name=name, sponsor=sponsor, memory=self.MEMORY, delay=delay, genus=genus) for variety in LeaderboardVariety ]
        return sorted(stream_boards + memory_boards)

    def leaderboard_name_as_dict(self, leaderboard_name):
        _, str_variety, str_values = leaderboard_name.split(SepConventions.sep())
        things = str_variety.split(SepConventions.pipe())
        values = str_values.split(SepConventions.pipe())
        return dict(zip(things, values))

    def leaderboard_memory_from_name(self,leaderboard_name:str) -> int:
        d = self.leaderboard_name_as_dict(leaderboard_name=leaderboard_name)
        return int(d[str(LeaderboardVariety.memory)]) if str(LeaderboardVariety.memory) in d else self.MEMORY


if __name__=='__main__':
    print(LeaderboardConventions().stream_leaderboard_names(name='bill', sponsor='mary',delay=72))