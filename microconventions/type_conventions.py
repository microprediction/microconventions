from typing import List, Union, Any, Optional
from enum import Enum
from pprint import pprint
import json
from collections import namedtuple
from copy import deepcopy

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


class Genre(StrEnum):
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


MEMO_FIELDS = ['activity','genre','success','execution','warned','message',
               'write_key','sender','recipient','data']
MEMO_DEFAULTS = [Activity.unknown, Genre.unknown, 1, -1, 0, None,
                 None, None, None, None]
MEMO_STR_CAST = ['activity','genre']
try:
    MemoType = namedtuple('MemoType',field_names=MEMO_FIELDS, defaults=MEMO_DEFAULTS)
except TypeError:
    # Prior to 3.7, we just proceed with no defaults.
    MemoType = namedtuple('MemoType', field_names=MEMO_FIELDS)


class Memo(MemoType):

    def to_dict(self,cast_to_str=True, leave_out_none=True, flatten_data=True):
        d = dict([ (k,v) for k,v in self._asdict().items() if v is not None ] ) if leave_out_none else self._asdict()
        if cast_to_str:
            for k in MEMO_STR_CAST:
                if k in d:
                    d[k] = str(d[k])
        if flatten_data and d.get('data') is not None:
            if isinstance(d.get('data'),dict):
                data = deepcopy(d['data'])
                d.update(data)
                del(d['data'])
        return d

    def __str__(self):
        return json.dumps(self.to_dict())

    def replace(self,**kwargs):
        return self._replace(**kwargs)


if __name__=="__main__":
    activity = Activity.submit
    print(activity)

    message = Memo(activity=Activity.set, genre=Genre.lagged, message='all good',data={'care':7,'dog':13})
    pprint(message.to_dict())
    message = message.replace(success=1)
    pprint(message.to_dict())

