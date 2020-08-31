from microconventions.sep_conventions import SepConventions
from enum import Enum


class RatingVariety(Enum):
    """ Enumerates varieties of leaderboards """
    memory = 0
    delay = 1

    def __str__(self):
        return super().__str__().split('.')[1]

    def split(self):
        return self.__str__().split('_and_')

    def instance_name(self, **kwargs):
        return SepConventions.pipe().join([str(kwargs[k]) for k in self.split()])


class RatingConventions(SepConventions):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.RATING = "rating" + self.SEP

    def rating_name(self, rating_variety, **kwargs):
        """ Name for rating tables
              variety:  RatingVariety
        """
        return self.RATING + str(rating_variety) + self.SEP + rating_variety.instance_name(**kwargs)


if __name__=='__main__':
    sc = RatingConventions()
    for variety in RatingVariety:
        print(variety)
        print(sc.rating_name(rating_variety=variety, name='bill', sponsor='mary', memory=10000, delay=72, host='home', genus='bivariate'))