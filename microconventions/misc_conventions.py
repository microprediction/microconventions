from microconventions.sep_conventions import SepConventions

class MiscConventions(SepConventions):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DELAYED = "delayed" + self.SEP
        self.CDF = 'cdf' + self.SEP
        self.LINKS = "links" + self.SEP
        self.BACKLINKS = "backlinks" + self.SEP
        self.MESSAGES = "messages" + self.SEP
        self.HISTORY = "history" + self.SEP
        self.LAGGED = "lagged" + self.SEP
        self.LAGGED_VALUES = "lagged_values" + self.SEP
        self.LAGGED_TIMES = "lagged_times" + self.SEP
        self.SUBSCRIBERS = "subscribers" + self.SEP
        self.SUBSCRIPTIONS = "subscriptions" + self.SEP
        self.TRANSACTIONS = "transactions" + self.SEP
        self.PREDICTIONS = "predictions" + self.SEP
        self.SAMPLES = "samples" + self.SEP
        self.BALANCE = "balance" + self.SEP
        self.PERFORMANCE = "performance" + self.SEP
        self.BUDGETS = "budget" + self.SEP
        self.VOLUMES = "volumes" + self.SEP
        self.SUMMARY = "summary" + self.SEP

        # Logging
        self.CONFIRMS = "confirms" + self.SEP
        self.WARNINGS = "warnings" + self.SEP
        self.ERRORS = "errors" + self.SEP

    def history_name(self, name):
        return self.HISTORY + name

    def lagged_values_name(self, name):
        return self.LAGGED_VALUES + name

    def lagged_times_name(self, name):
        return self.LAGGED_TIMES + name

    def links_name(self, name, delay):
        return self.LINKS + str(delay) + self.SEP + name

    def backlinks_name(self, name):
        return self.BACKLINKS + name

    def subscribers_name(self, name):
        return self.SUBSCRIBERS + name

    def subscriptions_name(self, name):
        return self.SUBSCRIPTIONS + name

    def cdf_name(self, name, delay=None):
        return self.CDF + name if delay == None else self.CDF + str(delay) + self.SEP + name


