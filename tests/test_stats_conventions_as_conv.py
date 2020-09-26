from microconventions.conventions import MicroConventions
import numpy as np


def test_cdf_invcdf():
    normcdf = MicroConventions._normcdf_function()
    norminv = MicroConventions._norminv_function()
    for x in np.random.randn(100):
        x1 = norminv(normcdf(x))
        assert abs(x - x1) < 1e-4


def test_mean_percentile():
    zscores = np.random.randn(100)
    normcdf = MicroConventions._normcdf_function()
    norminv = MicroConventions._norminv_function()
    p = [normcdf(z) for z in zscores]
    avg_p = MicroConventions.zmean_percentile(p)
    implied_avg = norminv(avg_p)
    actual_avg = np.mean(zscores)
    assert abs(implied_avg - actual_avg) < 1e-4


def test_absc():
    sc = MicroConventions(num_predictions=250)
    xs = sc.percentile_abscissa()
    assert len(xs) > 5
    xs = MicroConventions.percentile_abscissa()
    assert len(xs) > 5
