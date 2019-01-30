import graphene
from graphene import relay


class User(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    email = graphene.String()
    name = graphene.String()

    @classmethod
    def get_node(cls, info, id):
        return User()
