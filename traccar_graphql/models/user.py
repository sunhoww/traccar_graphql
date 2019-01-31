import graphene
from graphene import relay
from graphql import GraphQLError

from traccar_graphql import api, exceptions
from traccar_graphql.utils import request2object


class User(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    email = graphene.String()
    name = graphene.String()

    @classmethod
    def get_node(cls, info, id):
        return me()


def me():
    try:
        r = api.call("session")
        if r.status_code == 404:
            raise GraphQLError(exceptions.AUTHENTICATION_REQUIRED)
    except GraphQLError as e:
        # this exception might also be raised by api.call
        if e.message == exceptions.AUTHENTICATION_REQUIRED:
            return None
        raise e
    return request2object(r, User)
