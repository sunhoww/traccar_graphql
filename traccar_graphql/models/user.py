import graphene
from graphene import relay
from graphql import GraphQLError

from traccar_graphql import api
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
    r = api.call("session")
    if r.status_code == 404:
        raise GraphQLError("Authentication required")
    return request2object(r, User)
