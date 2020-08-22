from microconventions.zcurve_conventions import ZCurveConventions
import numpy as np


def test_morton():
    zc = ZCurveConventions()
    for dim in [2, 3]:
        for _ in range(100):
            prtcls = list(np.random.rand(dim))
            z = zc.to_zcurve(prctls=prtcls)
            prtcls_back = zc.from_zcurve(z, dim=len(prtcls))
            assert all(abs(p1 - p2) < 10. / zc.morton_scale(dim=3) for p1, p2 in
                       zip(prtcls, prtcls_back)), "Morton embedding failed "
