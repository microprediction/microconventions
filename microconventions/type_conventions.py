from typing import List, Union, Any, Optional
from enum import Enum
from pprint import pprint
import json

KeyList = List[Optional[str]]
NameList = List[Optional[str]]
Value = Union[str, int]
ValueList = List[Optional[Value]]
DelayList = List[Optional[int]]


class StrEnum(Enum):

    # Enum that prints itself with brevity

    def __str__(self):
        return super().__str__().split('.')[1]


class Activity(StrEnum):
    unknown = -1
    other = 0
    submit = 1
    set = 2
    mset = 3
    cset = 4
    give = 5
    receive = 6
    touch = 7
    mtouch = 8


class Resource(StrEnum):
    unknown = -1
    other = 0
    stream = 1
    cdf = 2
    lagged = 3
    errors = 4
    warnings = 5
    transactions = 6
    leaderboard = 7
    ratings = 8
    balance = 9
    prize = 10
    announcements = 11
    repository = 12
    messages = 13
    links = 14
    subscribers = 15


class Genus(StrEnum):
    regular = 0
    zscore = 1
    bivariate = 2
    trivariate = 3

    @staticmethod
    def from_name(name):
        return Genus.trivariate if 'z3~' in name else Genus.bivariate if 'z2~' in name else Genus.zscore if 'z1~' in name else Genus.regular


class Family(StrEnum):
    name = 0
    delay = 1
    genus = 2
    sponsor = 3

    def __str__(self):
        return super().__str__().split('.')[1]


class Memo:

    def __init__(self,activity:Activity=Activity.unknown,
                      resource:Resource=Resource.unknown,
                      success:int=1, warned:int=0, message:str='', data:dict=None, **kwargs ):
        self.activity = activity
        self.resource = resource
        self.success  = int(success)
        self.warned   = int(warned)
        self.message  = message
        data = data or dict()
        data.update(**kwargs)
        self.data     = data

    def to_dict(self):
        d = {"activity":str(self.activity),
            "resource":str(self.resource),
            "success":self.success,
            "message":self.message,
            "warned":self.warned}
        d.update(self.data)
        return d

    def __str__(self):
        return json.dumps(self.to_dict())


if __name__=="__main__":
    activity = Activity.submit
    print(activity)

    message = Memo(activity=Activity.set, resource=Resource.lagged, message='all good')
    pprint(message.to_dict())
    pprint(str(message))
