from typing import List, Union, Optional
from enum import Enum
from pprint import pprint
from collections import OrderedDict
from copy import deepcopy
import time, datetime

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
    put = 5
    touch = 6
    mtouch = 7
    delete = 8
    patch = 9


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


class Memo(OrderedDict):
    _STR_FIELDS = ['activity','genre']

    def __init__(self, activity:Activity,
                       genre:Genre,
                       epoch:float=None,
                       timestr:str=None,
                       write_key:str=None,
                       recipient:str=None,
                       success:int=1,
                       execution:int=-1,
                       count:int=None,
                       allowed:int=None,
                       message:str=None,
                       data:dict=None
                       ):
        self._initialized = False
        super().__init__(activity=activity,genre=genre,epoch=epoch,timestr=timestr,write_key=write_key,
                        recipient=recipient,success=success,execution=execution, count=count,allowed=allowed,
                         message=message, data=data)
        if self.get('epoch') is None:
            self['epoch'] = time.time()
        if self.get('timestr') is None:
            self['timestr'] = str(datetime.datetime.now())
        self._initialized = True

    def __setitem__(self, key, value):
        if self._initialized:
            if key not in self.keys():
                raise Exception(key+' is not a valid memo field')
            else:
                existing_value = self[key]
                if existing_value is None or type(value)==type(existing_value):
                    super().__setitem__(key,value)
                else:
                    raise Exception(key+' is supposed to be type '+str(type(existing_value)))
        else:
            super().__setitem__(key, value)

    def to_dict(self, cast_to_str=True, leave_out_none=True, flatten_data=True):
        d = OrderedDict([(k, v) for k, v in dict(self).items() if v is not None]) if leave_out_none else OrderedDict(self)
        if cast_to_str:
            for k in self._STR_FIELDS:
                if k in d:
                    d[k] = str(d[k])
        if flatten_data and d.get('data') is not None:
            if isinstance(d.get('data'), dict):
                data = deepcopy(d['data'])
                del(d['data'])
                d.update(data)
                return d
        return d


if __name__=="__main__":
    activity = Activity.submit
    print(activity)

    message = Memo(activity=Activity.set, genre=Genre.lagged, message='all good',data={'care':7,'dog':13})
    message['success'] = 1
    pprint(message.to_dict())
