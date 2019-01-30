from flask import current_app
import requests
from toolz import merge, dissoc

from traccar_graphql.utils import header_with_auth


def call(resource, method="GET", auth=True, **args):
    uri = "{traccar}/api/{resource}".format(
        traccar=current_app.config["TRACCAR_BACKEND"], resource=resource
    )
    return requests.request(
        method,
        uri,
        headers=merge(args.get("headers", {}), header_with_auth() if auth else {}),
        **dissoc(args, "headers"),
    )
