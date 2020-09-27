

class SepConventions(object):

    # Separators used in names

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.SEP   = SepConventions.sep()
        self.TILDE = SepConventions.tilde()

    @staticmethod
    def sep():
        return '::'

    @staticmethod
    def tilde():
        return '~'