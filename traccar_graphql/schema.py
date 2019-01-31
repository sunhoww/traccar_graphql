import graphene
from graphene import relay

from traccar_graphql import mutations
from traccar_graphql.models import user


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    me = graphene.Field(lambda: user.User, resolver=lambda *_: user.me())


class Mutation(graphene.ObjectType):
    login = mutations.Login.Field()
    logout = mutations.Logout.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
