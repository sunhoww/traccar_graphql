import json, re
from collections import namedtuple

_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')

def _to_snakes(key):
    s1 = _first_cap_re.sub(r'\1_\2', key)
    return _all_cap_re.sub(r'\1_\2', s1).lower()

def _object_hook(type):
    def hook(d):
        return namedtuple(type, map(_to_snakes, d.keys()))(*d.values())
    return hook

def request2object(res, type='GenericType'):
    return json.loads(res.text, object_hook=_object_hook(type))
