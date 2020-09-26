from microconventions.sep_conventions import SepConventions
from enum import Enum
from microconventions.type_conventions import StrEnum

class RatingVariety(StrEnum):
    """ Enumerates varieties of leaderboards """
    memory = 0
    delay = 1

    def split(self):
        return self.__str__().split('_and_')

    def instance_name(self, **kwargs):
        return SepConventions.pipe().join([str(kwargs[k]) for k in self.split()])


class RatingConventions(SepConventions):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.RATING = "rating" + self.SEP

    def rating_name(self, variety, **kwargs):
        """ Name for rating tables
              variety:  RatingVariety
        """
        return self.RATING + str(variety) + self.SEP + variety.instance_name(**kwargs)


if __name__=='__main__':
    sc = RatingConventions()
    for variety in RatingVariety:
        print(variety)
        print(sc.rating_name(variety=variety, name='bill', sponsor='mary', memory=10000, delay=72, host='home', genus='bivariate'))