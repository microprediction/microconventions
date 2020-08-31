from typing import List, Union, Any, Optional
from enum import Enum


KeyList = List[Optional[str]]
NameList = List[Optional[str]]
Value = Union[str, int]
ValueList = List[Optional[Value]]
DelayList = List[Optional[int]]


class Genus(Enum):
    regular = 0
    zscore = 1
    bivariate = 2
    trivariate = 3

    def __str__(self):
        return super().__str__().split('.')[1]

    @staticmethod
    def from_name(name):
        return Genus.trivariate if 'z3~' in name else Genus.bivariate if 'z2~' in name else Genus.zscore if 'z1~' in name else Genus.regular


class Family(Enum):
    name = 0
    delay = 1
    genus = 2
    sponsor = 3

    def __str__(self):
        return super().__str__().split('.')[1]




