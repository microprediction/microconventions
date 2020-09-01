from microconventions.rating_conventions import RatingVariety, RatingConventions\

def test_rating_names():
    rc = RatingConventions()
    for variety in RatingVariety:
        print(variety)
        print(rc.rating_name(variety=variety, name='bill', sponsor='mary', memory=10000, delay=72,
                             host='home', genus='bivariate'))

