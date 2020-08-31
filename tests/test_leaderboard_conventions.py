from microconventions.leaderboard_conventions import LeaderboardConventions, LeaderboardVariety


def test_leaderboard_names():
    lbc = LeaderboardConventions()
    lbs = lbc.stream_leaderboard_names(name='bill', sponsor='mary', delay=72)
    for lb in lbs:
        memory = lbc.leaderboard_memory_from_name(lb)
        print(memory)

