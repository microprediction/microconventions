from microconventions.stats_conventions import StatsConventions
import numpy as np

def test_cdf_invcdf():
    normcdf = StatsConventions._normcdf_function()
    norminv = StatsConventions._norminv_function()
    for x in np.random.randn(100):
        x1 = norminv(normcdf(x))
        assert abs(x-x1)<1e-4

def test_mean_percentile():
    zscores = np.random.randn(100)
    normcdf = StatsConventions._normcdf_function()
    norminv = StatsConventions._norminv_function()
    p = [ normcdf(z) for z in zscores ]
    avg_p = StatsConventions.zmean_percentile(p)
    implied_avg = norminv(avg_p)
    actual_avg  = np.mean(zscores)
    assert abs(implied_avg-actual_avg)<1e-4