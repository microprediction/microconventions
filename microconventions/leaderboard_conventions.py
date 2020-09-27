from microconventions.horizon_conventions import HorizonConventions
from microconventions.sep_conventions import SepConventions

class LeaderboardConventions(SepConventions):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.LEADERBOARD = "leaderboard" + self.SEP
        self.CUSTOM_LEADERBOARD = 'custom_leaderboard' + self.SEP

    def leaderboard_name(self, name=None, delay=None):
        """ Name for leaderboards by stream name and horizon """
        if name is None and delay is None:
            return self.LEADERBOARD[:-2]+'.json'
        elif name is None:
            return self.LEADERBOARD+str(delay)+'.json'
        elif delay is None:
            return self.LEADERBOARD+str(name)
        else:
            return self.LEADERBOARD+HorizonConventions.horizon_name(name=name,delay=delay)

    def custom_leaderboard_name(self, sponsor, name=None, dt=None):
        """ Names for leaderboards with a given sponsor
        :param sponsor:  str
        :param name:     str
        :param dt:       datetime
        :return:
        """

        def lb_cat(name=None):
            if name is not None:
                if 'z1~' in name:
                    return 'zscores_univariate'
                elif 'z2~' in name:
                    return 'zcurves_bivariate'
                elif 'z3~' in name:
                    return 'zcurves_trivariate'
                else:
                    return 'regular'
            else:
                return 'all_streams'

        def lb_month(dt=None):
            return dt.isoformat()[:7] if dt is not None else 'all_time'

        return self.SEP.join(
            [self.CUSTOM_LEADERBOARD[:-2], sponsor.replace(' ', '_'), lb_cat(name), lb_month(dt)]) + '.json'