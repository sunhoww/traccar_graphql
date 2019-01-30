import graphene
from graphene import relay

from traccar_graphql import mutations


class Query(graphene.ObjectType):
    node = relay.Node.Field()


class Mutation(graphene.ObjectType):
    login = mutations.Login.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
