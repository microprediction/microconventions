import numpy as np


class StatsConventions:

    # Statistics standard library introduced normal distribution but only in versions above 3.8
    # This adds a tiny amount of backward compatability but note that scipy is not a formal dependency so some users
    # will need to install that of their own volition. Python caches imports so don't worry too much about this.

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def normcdf(x):
        g = StatsConventions._normcdf_function()
        return g(x)

    @staticmethod
    def norminv(p):
        f = StatsConventions._norminv_function()
        return f(p)

    @staticmethod
    def _norminv_function():
        try:
            from statistics import NormalDist
            return NormalDist(mu=0, sigma=1.0).inv_cdf
        except ImportError:
            from scipy.stats import norm
            return norm.ppf

    @staticmethod
    def _normcdf_function():
        try:
            from statistics import NormalDist
            return NormalDist(mu=0, sigma=1.0).cdf
        except ImportError:
            from scipy.stats import norm
            return norm.cdf

    @staticmethod
    def zmean_percentile(ps):
        """ A convention for summarizing percentile data
            :param ps [float]   values in (0,1)
            :returns float
        """
        # TODO: Make more robust when there are 0's and 1's

        if len(ps):
            zscores = [ StatsConventions.norminv(p) for p in ps]
            avg_zscore = np.nanmean(zscores)
            return StatsConventions.normcdf(avg_zscore)
        else:
            return 0.5

    @staticmethod
    def percentile_abscissa():
        """ Default x-values for cdf """
        # Lagged values are also used
        return [-2.3263478740408408, -1.6368267885518997, -1.330561513178897, -1.1146510149326596,
         -0.941074530352976, -0.792046894425591, -0.6588376927361878, -0.5364223812298266,
         -0.4215776353171568, -0.3120533220328322, -0.20615905948527324, -0.10253336200497987, 0.0,
         0.10253336200497973, 0.20615905948527324, 0.31205332203283237, 0.4215776353171568,
         0.5364223812298264, 0.6588376927361878, 0.7920468944255913, 0.941074530352976, 1.1146510149326592,
         1.330561513178897, 1.6368267885519001, 2.3263478740408408]