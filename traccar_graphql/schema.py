import os, graphene, requests
from flask_jwt_extended import get_jwt_claims
from graphql import GraphQLError

from traccar_graphql.models import ServerType, UserType, GroupType
from traccar_graphql.mutations import LoginType, RegisterType, CreateGroupType
from traccar_graphql.loaders import group_loader
from traccar_graphql.utils import request2object, header_with_auth

TRACCAR_BACKEND = os.environ.get('TRACCAR_BACKEND')

class Query(graphene.ObjectType):
    server = graphene.Field(lambda: ServerType)
    def resolve_server(self, args, context, info):
        r = requests.get("{}/api/server".format(TRACCAR_BACKEND))
        return request2object(r, 'ServerType')

    me = graphene.Field(lambda: UserType)
    def resolve_me(self, args, context, info):
        r = requests.get(
            "{}/api/session".format(TRACCAR_BACKEND),
            headers=header_with_auth()
            )
        if r.status_code == 404:
            raise GraphQLError('Authentication required')
        return request2object(r, 'UserType')

    group = graphene.Field(lambda: GroupType, id=graphene.Int())
    def resolve_group(self, args, context, info):
        return group_loader.load(args.get('id'))

    # TODO: figure out a way for this to use the group_loader as well
    all_groups = graphene.List(lambda: GroupType)
    def resolve_all_groups(self, args, context, info):
        r = requests.get(
            "{}/api/groups".format(TRACCAR_BACKEND),
            headers=header_with_auth()
            )
        return request2object(r, 'GroupType')

class Mutation(graphene.ObjectType):
    login = LoginType.Field()
    register = RegisterType.Field()
    create_group = CreateGroupType.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
