from microconventions.leaderboard_conventions import LeaderboardConventions, LeaderboardVariety


def test_leaderboard_names():
    lbc = LeaderboardConventions()
    lbs = lbc.leaderboard_names_to_update(name='bill', sponsor='mary', delay=72)
    for lb in lbs:
        memory = lbc.leaderboard_memory_from_name(lb)
        print(memory)

def test_this():
    lbc = LeaderboardConventions()
    lb_names = lbc.leaderboard_names_to_update(name='bill', sponsor='mary', delay=72)
    lb_dicts = [lbc.leaderboard_name_as_dict(name) for name in lb_names]

    expected = [{'delay': 72}, {'genus': 'regular'}] + [{'memory': memory} for memory in lbc.LEADERBOARD_MEMORIES] + [{'name': 'bill'},
                                                                                                                      {'delay': 72, 'name': 'bill'},
                                                                                                                      {'sponsor': 'mary'},
                                                                                                                      {'delay': 72, 'sponsor': 'mary'},
                                                                                                                      {'genus': 'regular', 'sponsor': 'mary'}]
    for lbd, expected_lbd in zip(lb_dicts,expected):
        assert lbd==expected_lbd or 'memory' in lbd
