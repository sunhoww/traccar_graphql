import os, graphene, requests
from flask_jwt_extended import get_jwt_identity, get_jwt_claims
from graphql import GraphQLError

from traccar_graphql.models import ServerType, UserType
from traccar_graphql.mutations import LoginType, RegisterType
from traccar_graphql.utils import request2object

TRACCAR_BACKEND = os.environ.get('TRACCAR_BACKEND')

class Query(graphene.ObjectType):
    server = graphene.Field(lambda: ServerType)
    me = graphene.Field(lambda: UserType)
    def resolve_server(self, args, context, info):
        r = requests.get("{}/api/server".format(TRACCAR_BACKEND))
        return request2object(r, 'ServerType')
    def resolve_me(self, args, context, info):
        claims = get_jwt_claims()
        if 'session' not in claims:
            raise GraphQLError('Authentication required')
        headers = { 'Cookie': claims['session'] }
        r = requests.get("{}/api/session".format(TRACCAR_BACKEND), headers=headers)
        return request2object(r, 'UserType')

class Mutation(graphene.ObjectType):
    login = LoginType.Field()
    register = RegisterType.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
