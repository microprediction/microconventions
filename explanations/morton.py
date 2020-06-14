from microconventions.zcurve_conventions import ZCurveConventions
import numpy as np

def show_morton_distribution():
    """ Visually verify that zcurves are N(0,1) for the independent case """
    zc = ZCurveConventions()
    import matplotlib.pyplot as plt
    from scipy.stats import probplot
    zs = list()
    for dim in [2, 3]:
        for _ in range(10000):
            prtcls = list(np.random.rand(dim))
            z = zc.to_zcurve(prctls=prtcls)
            zs.append(z)
    probplot(zs,plot=plt)
    plt.show()

if __name__=="__main__":
    show_morton_distribution()