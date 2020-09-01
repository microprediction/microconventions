from microconventions.type_conventions import List
from microconventions.sep_conventions import SepConventions


class HorizonConventions:

    def __init__(self, delays: List[int], **kwargs):
        super().__init__(**kwargs)
        self.DELAYS = delays

    @staticmethod
    def horizon_name(name, delay):
        """ Convention is used for performance and other hashes """
        return str(delay) + SepConventions.sep() + name

    @staticmethod
    def split_horizon_name(horizon):
        spl = horizon.split(SepConventions.sep())
        name = spl[1]
        delay = int(spl[0])
        return name, delay

    def split_horizon_names(self, horizons):
        names_delays = [self.split_horizon_name(key) for key in horizons]
        names = [n for n, _ in names_delays]
        delays = [d for _, d in names_delays]
        return names, delays

    @staticmethod
    def delay_from_horizon(horizon):
        return int(horizon.split(SepConventions.sep())[0])

    @staticmethod
    def name_from_horizon(horizon):
        return horizon.split(SepConventions.sep())[1]
