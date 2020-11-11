import re

COORDINATES = re.compile(r'(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)$')


def valid_location(location):
    return COORDINATES.match(location)


def radius_in_range(radius):
    return len(str(radius)) <= 4


def valid_keyword(keyword):
    return len(keyword) <= 128


def has_key(obj, key):
    return key in obj.keys()
