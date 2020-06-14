import re, uuid
from microconventions.misc_conventions import MiscConventions

class StreamConventions(object):
    # Conventions for names of streams

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def sep():
        return '::'

    @staticmethod
    def is_plain_name(name: str):
        return StreamConventions.is_valid_name(name) and not "~" in name

    @staticmethod
    def is_valid_name(name: str):
        name_regex = re.compile(r'^[-a-zA-Z0-9_~.:]{1,200}\.[json,html]+$', re.IGNORECASE)
        return (re.match(name_regex, name) is not None) and (not StreamConventions.sep() in name)

    @staticmethod
    def random_name():
        return str(uuid.uuid4()) + '.json'

