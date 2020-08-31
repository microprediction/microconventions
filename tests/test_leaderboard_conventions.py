from microconventions.leaderboard_conventions import LeaderboardConventions, LeaderboardVariety


def test_leaderboard_names():
    lb = LeaderboardConventions()
    for variety in LeaderboardVariety:
        print(variety)
        print(lb.leaderboard_name(leaderboard_variety=variety, name='bill', sponsor='mary', memory=10000, delay=72,
                                  host='home', genus='bivariate'))

