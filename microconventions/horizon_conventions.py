from microconventions.type_conventions import List
from microconventions.sep_conventions import SepConventions

class HorizonConventions(SepConventions):

    def __init__(self,delays:List[int],**kwargs):
        super().__init__(**kwargs)
        self.DELAYS = delays

    @staticmethod
    def horizon_name(name, delay):
        """ Convention is used for performance and other hashes """
        return str(delay) + SepConventions.sep() + name

    @staticmethod
    def split_horizon_name(key):
        spl = key.split(SepConventions.sep())
        name = spl[1]
        delay = int(spl[0])
        return name, delay
