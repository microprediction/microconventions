import json, sys
import numpy as np
from json.decoder import JSONDecodeError
from deepdiff import DeepDiff

# Conventions about published values


class ValueConventions(object):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def is_scalar_value(value):
        try:
            fv = float(value)
            return True
        except:
            return False

    @staticmethod
    def is_valid_value(value):
        return isinstance(value, (str, int, float)) and sys.getsizeof(value) < 100000

    @staticmethod
    def is_small_value(value):
        """ Used to determine how to store history for dict like values """
        return sys.getsizeof(value) < 1200

    @staticmethod
    def is_vector_value(value):
        if isinstance(value, (list, tuple)):
            return all((ValueConventions.is_scalar_value(v) for v in value))
        else:
            try:
                v = json.loads(value)
                return ValueConventions.is_vector_value(v)
            except:
                return False

    @staticmethod
    def is_dict_value(value):
        try:
            d = dict(value)
            return True
        except:
            try:
                v = json.loads(value)
                return ValueConventions.is_dict_value(value)
            except:
                return False

    @staticmethod
    def to_record(value):
        if ValueConventions.is_scalar_value(value):
            fields = {"0": value}
        elif ValueConventions.is_dict_value(value):
            fields = dict(value)
        elif ValueConventions.is_vector_value(value):
            fields = dict(enumerate(list(value)))
        else:
            fields = {"value": value}
        return fields

    @staticmethod
    def has_nan(obj):
        if isinstance(obj, (list,tuple)):
            return any(map(ValueConventions.has_nan, obj))
        elif isinstance(obj, dict):
            return ValueConventions.has_nan(list(obj.values())) or ValueConventions.has_nan(list(obj.keys()))
        else:
            try:
                return np.isnan(obj)
            except (TypeError, JSONDecodeError):
                return False

    @staticmethod
    def deep_equal(obj1, obj2):
        return not DeepDiff(obj1, obj2, ignore_order=True)