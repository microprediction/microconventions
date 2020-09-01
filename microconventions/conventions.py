from getjson import getjson
from microconventions.stats_conventions import StatsConventions
from microconventions.key_conventions import KeyConventions
from microconventions.stream_conventions import StreamConventions
from microconventions.leaderboard_conventions import LeaderboardConventions, LeaderboardVariety
from microconventions.rating_conventions import RatingConventions, RatingVariety
from microconventions.value_conventions import ValueConventions
from microconventions.zcurve_conventions import ZCurveConventions
from microconventions.misc_conventions import MiscConventions
from microconventions.horizon_conventions import HorizonConventions
from microconventions.budget_conventions import BudgetConventions
from microconventions.url_conventions import api_url, failover_api_url, get_config, connected_to_internet
import requests


# BudgetConventions must be listed last here
class MicroConventions(StreamConventions, HorizonConventions, ValueConventions, MiscConventions, ZCurveConventions,
                       LeaderboardConventions, RatingConventions, StatsConventions, BudgetConventions):

    def __init__(self, base_url=None, num_predictions=None, min_len=None, min_balance=None, delays=None,
                 failover_base_url=None):
        """ If not all arguments are supplied they will be grabbed from Microprediction.Org """

        self.base_url = base_url or api_url()
        self.failover_base_url = failover_base_url or failover_api_url()
        if any(parameter is None for parameter in [num_predictions, min_len, min_balance]):
            config = get_config()
            if config is None:
                if not connected_to_internet():
                    raise Exception('Cannot initialize without internet access if parameters are not supplied. Maybe check that your internet connection is working.')
                else:
                    raise Exception('Could not initialize. Possibly due to slow internet. Maybe try again in a couple of moments.')
        self.num_predictions = num_predictions or config["num_predictions"]

        # Pass arguments through to mixins
        delays = delays or config['delays']
        min_len = min_len or config["min_len"]
        min_balance = min_len or config["min_balance"]
        super().__init__(delays=delays, min_difficulty=min_len, min_balance=min_balance)

    def request_get_json(self, method, arg=None, data=None, throw=True):
        """ Canonical way to call methods using requests library """
        try:
            if data is not None:
                res = requests.get(self.base_url + '/' + method + '/' + arg, data=data)
            elif arg is not None:
                res = requests.get(self.base_url + '/' + method + '/' + arg)
            elif data is None and arg is None:
                res = requests.get(self.base_url + '/' + method)
            if res.status_code == 200:
                return res.json()
        except ConnectionError as e:
            print('WARNING: ConnectionError attempting to get ' + method)
            if throw:
                raise e

