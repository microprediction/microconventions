import numpy as np
from tdigest import TDigest
import math


class StatsConventions:

    # Statistics standard library introduced normal distribution but only in versions above 3.8
    # This adds a tiny amount of backward compatability but note that scipy is not a formal dependency so some users
    # will need to install that of their own volition. Python caches imports so don't worry too much about this.

    def __init__(self, num_predictions, **kwargs):
        super().__init__(**kwargs)
        self.num_predictions = num_predictions

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
            zscores = [StatsConventions.norminv(p) for p in ps]
            avg_zscore = np.nanmean(zscores)
            return StatsConventions.normcdf(avg_zscore)
        else:
            return 0.5

    @staticmethod
    def percentile_abscissa():
        """ Default x-values for cdf """
        # Deprecated
        return [-2.3263478740408408, -1.6368267885518997, -1.330561513178897, -1.1146510149326596,
                -0.941074530352976, -0.792046894425591, -0.6588376927361878, -0.5364223812298266,
                -0.4215776353171568, -0.3120533220328322, -0.20615905948527324, -0.10253336200497987, 0.0,
                0.10253336200497973, 0.20615905948527324, 0.31205332203283237, 0.4215776353171568,
                0.5364223812298264, 0.6588376927361878, 0.7920468944255913, 0.941074530352976, 1.1146510149326592,
                1.330561513178897, 1.6368267885519001, 2.3263478740408408]

    # -------------------------------------------------------------------------------------
    # Utilities for constructing representative values that might be taken by a time series
    # -------------------------------------------------------------------------------------
    # Need this to provide canonical CDF methods
    # Also for rudimentary default benchmark predictions

    @staticmethod
    def is_discrete(lagged_values, num, ndigits=12):
        """
              num     Maximum number of unique values before it is considered continuous
        """
        return len(set([round(x, ndigits) for x in lagged_values])) <= num

    @staticmethod
    def evenly_spaced_percentiles(num):
        return list(np.linspace(start=1 / (2 * num), stop=1 - 1 / (2 * num), num=num))
        # [1. / (2 * num)] + list(1. / (2 * num) + np.cumsum((1 / num) * np.ones(num - 1)))

    @staticmethod
    def sign_changes(lagged_values):
        return np.nansum([abs(d) > 1.5 for d in np.diff(np.sign(list(lagged_values) + [0., 0.]))])

    @staticmethod
    def is_process(lagged_values):
        " Placeholder for something better :-) "
        return StatsConventions.sign_changes(np.diff(lagged_values)) > 2 * StatsConventions.sign_changes(lagged_values)

    @staticmethod
    def cdf_values(lagged_values: [float], num, as_discrete=None):
        """ Default method of determining which abscissa are used for CDF's

                    as_discrete   Whether discrete values only are taken

        """
        if as_discrete is None:
            as_discrete = StatsConventions.is_discrete(lagged_values=lagged_values, num=num)

        if as_discrete:
            return StatsConventions._cdf_discrete_values(lagged_values=lagged_values, num=num)
        else:
            return StatsConventions._cdf_continuous_values(lagged_values=lagged_values, num=num)

    @staticmethod
    def _cdf_continuous_values(lagged_values: [float], num: int = None, ndigits=2, digest=None) -> [float]:
        """ Returns a list of example values the time series might take next, based on recent lags

               num       Maximum number of sample values
               decimals  How to round values, which can be useful in reducing the number of calls
               machine   Supply an existing distribution machine to update it rather than starting afresh
               returns:  List of values of length not longer than num

        """
        # Uses t-digest
        # See
        digest = digest or TDigest()
        chronological_values = list(reversed(lagged_values))
        as_process = StatsConventions.is_process(chronological_values)
        xs = list(np.diff([0.] + chronological_values)) if as_process else chronological_values
        for x in xs:
            digest.update(x=x)
        sample_x = [digest.percentile(p * 100.) for p in StatsConventions.evenly_spaced_percentiles(num=num)]
        rounded_x = [round(x, ndigits) for x in sample_x]
        unique_x = list(set(rounded_x))
        return unique_x if not as_process else [chronological_values[-1] + x for x in unique_x]

    @staticmethod
    def _cdf_discrete_values(lagged_values: [float], num: int = 26, ndigits=6):
        chronological_values = list(reversed(lagged_values))
        as_process = StatsConventions.is_process(chronological_values)
        xs = list(np.diff([0.] + chronological_values)) if as_process else chronological_values
        return StatsConventions.quantize(xs, num=num, ndigits=ndigits)

    @staticmethod
    def discrete_pdf(ys: [float]):
        """ Imply PDF from CDF in the discrete case only

               ys   Cumulative probabilities returned by get_cdf

        """
        # The get_cdf method is designed for continuous distributions.
        # In the case of discrete distributions it can be misleading.
        # We can recover the PDF in the special case where CDF x-values
        # are chosen to equal the finite set of values taken.
        # See https://gist.github.com/microprediction/ea63388c2bbcfd7623bd9937723565b9
        # for a worked example
        num = len(ys)
        mij = [[4 * math.pow(-1, i + k) for i in range(k)] + [2] + [0] * (num - k - 1) for k in range(num)]
        M = np.array(mij)
        pdf = np.matmul(M, ys)
        return list(pdf)

    @staticmethod
    def discrete_cdf(cdf):
        """ Takes a raw CDF on discrete data and fixes it """
        pdf = StatsConventions.discrete_pdf(cdf['y'])
        h = np.min(np.diff(cdf['x'])) / 10.0
        below = zip([x - h for x in cdf['x']], [0] + pdf[:-1])
        above = zip([x + h for x in cdf['x']], pdf)
        pairs = sorted(list(below) + list(above))
        xs = [p[0] for p in pairs]
        ys = [p[1] for p in pairs]
        return {'x': xs, 'y': ys}

    @staticmethod
    def quantize(xs, num: int, ndigits: int = 12):
        """ Round until there are less than or equal to num items

                ndigits   Level of rounding to start at

        """
        if len(xs) <= num:
            return xs

        kdigits = ndigits
        while True:
            quantized_xs = set([round(x, kdigits) for x in xs])
            if len(quantized_xs) <= num:
                break
            kdigits = kdigits - 1

        return list(quantized_xs)

    @staticmethod
    def nudged(xs):
        """ Bump samples around just a little """
        noise = np.random.randn(len(xs))
        xs_sorted = sorted([s + 0.00001 * z for s, z in zip(xs, noise)])
        min_x = xs[0]
        max_x = xs[-1]
        eps = (max_x - min_x) / 1000
        xs_extended = [min_x - 10 * eps] + list(xs_sorted) + [max_x + eps * 10]
        xs_right = xs_extended[2:]
        xs_left = xs_extended[:-2]

        def _nudge(x, x_left, x_right, eps):
            if abs(x - x_left) < eps:
                if abs(x_right - x) > 3 * eps:
                    return x + eps
                else:
                    return (x_right + x) / 2.
            if abs(x_right - x) < eps:
                if abs(x - x_left) > 3 * eps:
                    return x - eps
                else:
                    return (x + x_left) / 2.
            return x

        return [_nudge(x, xl, xr, eps) for x, xl, xr in zip(xs_sorted, xs_left, xs_right)]


nudged = StatsConventions.nudged
is_discrete = StatsConventions.is_discrete
evenly_spaced_percentiles = StatsConventions.evenly_spaced_percentiles
cdf_values = StatsConventions.cdf_values
quantize = StatsConventions.quantize
discrete_pdf = StatsConventions.discrete_pdf
discrete_cdf = StatsConventions.discrete_cdf
is_process = StatsConventions.is_process
sign_changes = StatsConventions.sign_changes


if __name__ == '__main__':
    x = [-3., 0., 0., 0., 0., 0., 1.]
    y = StatsConventions.nudged(x)
