import re

COORDINATES = re.compile(r'(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)$')


def valid_location(location):
    return False if not COORDINATES.match(location) else True


def valid_address(address):
    return address is not None and len(address) <= 128


def radius_in_range(radius):
    return len(str(radius)) <= 4


def valid_keyword(keyword):
    return len(keyword) <= 128


def has_key(obj, key):
    return key in obj.keys()
