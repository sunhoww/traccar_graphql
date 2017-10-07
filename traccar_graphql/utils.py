import json, re
from collections import namedtuple
from graphql import GraphQLError

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
    try:
        return json.loads(res.text, object_hook=_object_hook(type))
    except ValueError as e:
        raise GraphQLError(res.text)


from flask_jwt_extended import get_jwt_claims

def header_with_auth():
    claims = get_jwt_claims()
    if 'session' not in claims:
        raise GraphQLError('Authentication required')
    return { 'Cookie': claims['session'] }

def _to_camels(key):
    words = key.split('_')
    return words[0] + ''.join(x.title() for x in words[1:])

def camelify_keys(d):
    camelized = {}
    if isinstance(d, dict):
        for k, v in d.items():
            camelized[_to_camels(k)] = camelify_keys(v)
    elif isinstance(d, list):
        vlist = []
        for v in d:
            if isinstance(v, (list, dict)):
                vlist.append(camelify_keys(v))
            else:
                vlist.append(v)
        return vlist
    else:
        return d
    return camelized
