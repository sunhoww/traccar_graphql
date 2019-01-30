import json
import re
from graphene import ObjectType
from graphql import GraphQLError
from flask_jwt_extended import get_jwt_claims

from collections import namedtuple

_first_cap_re = re.compile("(.)([A-Z][a-z]+)")
_all_cap_re = re.compile("([a-z0-9])([A-Z])")


def _to_snakes(key):
    s1 = _first_cap_re.sub(r"\1_\2", key)
    return _all_cap_re.sub(r"\1_\2", s1).lower()


def _object_hook(type):
    def hook(d):
        if not isinstance(type, str) and issubclass(type, ObjectType):
            return type(**{field: d.get(field) for field in type._meta.fields.keys()})
        return namedtuple(type, map(_to_snakes, d.keys()))(*d.values())

    return hook


def request2object(res, type="GenericType"):
    """ This func takes converts the dict from res.json() to an object
    Also converts camelCase keys to snake_case fields

    Args:
        res(:obj): A response object return by the `requests` library
        type(str, optional): The name of the object being constructed

    Returns:
        An object with deep mapped fields generated from the dict keys

    Raises:
        A GraphQLError with message from the `requests` response text
    """
    try:
        return json.loads(res.text, object_hook=_object_hook(type))
    except ValueError:
        raise GraphQLError(res.text)


def dict2object(d, type="GenericType"):
    return _object_hook(type)(d)


def camelify(key):
    words = key.split("_")
    return words[0] + "".join(x.title() for x in words[1:])


def camelify_keys(d):
    """ Converts snake_cased keys of a dict to camelCased ones

    Args:
        d(:dict, any): Initially a dict, but can be other types as well on
            further recursion

    Returns:
        A dict with camelCased keys
    """
    camelized = {}
    if isinstance(d, dict):
        for k, v in d.items():
            camelized[camelify(k)] = camelify_keys(v)
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


def header_with_auth():
    """ Generates a request header dict with a session cookie to be consumed
    by the backend

    Returns:
        A dict with key `Cookie` set to a value obtained from jwt claims
    """
    claims = get_jwt_claims()
    if "session" not in claims:
        raise GraphQLError("Authentication required")
    return {"Cookie": claims["session"]}


def current_user_id():
    """ Generates the user_id of the current user

    Returns:
        An int set to a value obtained from jwt claims
    """
    claims = get_jwt_claims()
    if "id" not in claims:
        raise GraphQLError("Authentication required")
    return claims["id"]


# TODO: Using an in-memory implementaion for now. Change to a more persistent
# storage
_blacklist = set()


def blacklist_token(jti):
    """ Generates a list of revoked and blacklisted tokens

    Returns:
        A list of blacklisted `jti`
    """
    _blacklist.add(jti)


def get_blacklisted_tokens():
    """ Generates a list of revoked and blacklisted tokens

    Returns:
        A list of blacklisted `jti`
    """
    return _blacklist
