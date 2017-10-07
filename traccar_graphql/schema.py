import os, graphene, requests
from flask_jwt_extended import get_jwt_claims
from graphql import GraphQLError

from traccar_graphql import models, mutations
from traccar_graphql.loaders import group_loader, driver_loader
from traccar_graphql.utils import request2object, header_with_auth

TRACCAR_BACKEND = os.environ.get('TRACCAR_BACKEND')

class Query(graphene.ObjectType):
    server = graphene.Field(lambda: models.ServerType)
    def resolve_server(self, args, context, info):
        r = requests.get("{}/api/server".format(TRACCAR_BACKEND))
        return request2object(r, 'ServerType')

    me = graphene.Field(lambda: models.UserType)
    def resolve_me(self, args, context, info):
        r = requests.get(
            "{}/api/session".format(TRACCAR_BACKEND),
            headers=header_with_auth())
        if r.status_code == 404:
            raise GraphQLError('Authentication required')
        return request2object(r, 'UserType')

    group = graphene.Field(lambda: models.GroupType, id=graphene.Int())
    def resolve_group(self, args, context, info):
        return group_loader.load(args.get('id'))

    # TODO: figure out a way for this to use the group_loader as well
    all_groups = graphene.List(lambda: models.GroupType)
    def resolve_all_groups(self, args, context, info):
        r = requests.get(
            "{}/api/groups".format(TRACCAR_BACKEND),
            headers=header_with_auth())
        return request2object(r, 'GroupType')

    driver = graphene.Field(lambda: models.DriverType, id=graphene.Int())
    def resolve_driver(self, args, context, info):
        return driver_loader.load(args.get('id'))

    all_drivers = graphene.List(lambda: models.DriverType)
    def resolve_all_drivers(self, args, context, info):
        r = requests.get(
            "{}/api/drivers".format(TRACCAR_BACKEND),
            headers=header_with_auth())
        return request2object(r, 'DriverType')

class Mutation(graphene.ObjectType):
    login = mutations.LoginType.Field()
    register = mutations.RegisterType.Field()
    create_group = mutations.CreateGroupType.Field()
    update_group = mutations.UpdateGroupType.Field()
    delete_group = mutations.DeleteGroupType.Field()
    create_driver = mutations.CreateDriverType.Field()
    update_driver = mutations.UpdateDriverType.Field()
    delete_driver = mutations.DeleteDriverType.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
