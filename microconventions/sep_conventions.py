class SepConventions(object):

    # Separators used in names, external and internal

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SEP = SepConventions.sep()
        self.TILDE = SepConventions.tilde()
        self.PIPE = SepConventions.pipe()

    @staticmethod
    def sep():
        return '::'

    @staticmethod
    def tilde():
        return '~'

    @staticmethod
    def pipe():
        return '|'
