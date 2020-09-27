from microconventions import MicroConventions

def test_misc():
    mc = MicroConventions()
    assert mc.DELAYED=='delayed::'
    assert mc.HISTORY=='history::'
    assert mc.BACKLINKS=='backlinks::'
    assert mc.LAGGED=='lagged::'
    assert mc.LAGGED_VALUES=='lagged_values::'
    assert mc.LAGGED_TIMES=='lagged_times::'
    assert mc.SUBSCRIBERS=='subscribers::'



def test_delays():
    mc = MicroConventions()
    assert len(mc.DELAYS)==4

def test_delays():
    mc = MicroConventions()
    assert len(mc.DELAYS)==4
