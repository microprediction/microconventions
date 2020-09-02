from microconventions.sep_conventions import SepConventions
from enum import Enum
from microconventions.type_conventions import Genus
from pprint import pprint
from collections import OrderedDict
from microconventions.horizon_conventions import HorizonConventions
from microconventions.type_conventions import StrEnum


class LeaderboardVariety(StrEnum):
    """ Enumerates varieties of leaderboards """
    memory = 0
    delay = 1
    name = 2
    sponsor = 3
    genus = 4
    name_and_delay = 21
    sponsor_and_delay = 31
    sponsor_and_genus = 34

    def split(self):
        return self.__str__().split('_and_')

    def instance_name(self, **kwargs):
        return SepConventions.pipe().join( [ str(kwargs[k]) for k in self.split() ])


class LeaderboardConventions(SepConventions):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LEADERBOARD = "leaderboard" + self.SEP
        self.CUSTOM_LEADERBOARD = 'custom_leaderboard' + self.SEP  # Deprecated
        self.LEADERBOARD_MEMORIES = OrderedDict({'movers':1000, 'default':10000, 'long':100000})
        self.LEADERBOARD_CAST = {'memory':int,'delay':int,'name':str,'sponsor':str,'genus':str}

    def leaderboard_name(self, variety:LeaderboardVariety, **kwargs):
        """ Name for leaderboards """
        return self.LEADERBOARD + str(variety) + self.SEP + variety.instance_name(**kwargs)

    def leaderboard_name_from_description(self, description='default'):
        """ e.g.  default, long, movers """
        return self.leaderboard_name(variety=LeaderboardVariety.memory,memory=self.LEADERBOARD_MEMORIES[description])

    def leaderboard_name_for_horizon(self, horizon):
        name, delay = HorizonConventions.split_horizon_name(horizon)
        return self.leaderboard_name(variety=LeaderboardVariety.name_and_delay, name=name, delay=delay )

    def leaderboard_names_to_update(self, name, sponsor, delay):
        """ Leaderboards that update when data arrives """
        genus = Genus.from_name(name=name)
        memory_boards = [self.leaderboard_name(variety=LeaderboardVariety.memory, memory=memory) for memory in self.LEADERBOARD_MEMORIES.values()]
        stream_boards = [self.leaderboard_name(variety=variety, name=name, sponsor=sponsor, memory=self.LEADERBOARD_MEMORIES['default'], delay=delay, genus=genus) for variety in LeaderboardVariety]
        return sorted(list(set(stream_boards + memory_boards)))

    def leaderboard_name_as_dict(self, leaderboard_name):
        """ leaderboard::name_and_delay::john.json|310  ->  {name:john.json,delay:310}"""
        _, str_variety, str_values = leaderboard_name.split(SepConventions.sep())
        things = str_variety.split('_and_')
        values = str_values.split(SepConventions.pipe())
        return dict([ (k,self.LEADERBOARD_CAST[k](v)) for k,v in zip(things, values)])

    def leaderboard_memory_from_name(self,leaderboard_name:str) -> int:
        d = self.leaderboard_name_as_dict(leaderboard_name=leaderboard_name)
        return int(d[str(LeaderboardVariety.memory)]) if str(LeaderboardVariety.memory) in d else self.LEADERBOARD_MEMORIES['default']


if __name__=='__main__':
    lbc = LeaderboardConventions()
    lb_names = lbc.leaderboard_names_to_update(name='bill', sponsor='mary', delay=72)
    lb_dicts = [lbc.leaderboard_name_as_dict(name) for name in lb_names]
    pprint((lb_dicts))