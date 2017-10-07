import os, graphene, requests
from flask_jwt_extended import get_jwt_claims
from graphql import GraphQLError

from traccar_graphql import models, mutations
from traccar_graphql.loaders import group_loader, driver_loader, geofence_loader, notification_loader
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

    geofence = graphene.Field(lambda: models.GeofenceType, id=graphene.Int())
    def resolve_geofence(self, args, context, info):
        return geofence_loader.load(args.get('id'))

    all_geofences = graphene.List(lambda: models.GeofenceType)
    def resolve_all_geofences(self, args, context, info):
        r = requests.get(
            "{}/api/geofences".format(TRACCAR_BACKEND),
            headers=header_with_auth())
        return request2object(r, 'GeofenceType')

    calendar = graphene.Field(lambda: models.CalendarType, id=graphene.Int())
    def resolve_calendar(self, args, context, info):
        return calendar_loader.load(args.get('id'))

    all_calendars = graphene.List(lambda: models.CalendarType)
    def resolve_all_calendars(self, args, context, info):
        r = requests.get(
            "{}/api/calendars".format(TRACCAR_BACKEND),
            headers=header_with_auth())
        return request2object(r, 'CalendarType')

    # TODO: figure out a way to change this arg name to 'type'
    notification = graphene.Field(lambda: models.NotificationType, notification_type=graphene.String())
    def resolve_notification(self, args, context, info):
        return notification_loader.load(args.get('notification_type'))

    all_notification_types = graphene.List(lambda: models.NotificationTypeType)
    def resolve_all_notification_types(self, args, context, info):
        r = requests.get(
            "{}/api/users/notifications".format(TRACCAR_BACKEND),
            headers=header_with_auth())
        print(r.text)
        return request2object(r, 'NotificationTypeType')


class Mutation(graphene.ObjectType):
    login = mutations.LoginType.Field()
    register = mutations.RegisterType.Field()
    create_group = mutations.CreateGroupType.Field()
    update_group = mutations.UpdateGroupType.Field()
    delete_group = mutations.DeleteGroupType.Field()
    create_driver = mutations.CreateDriverType.Field()
    update_driver = mutations.UpdateDriverType.Field()
    delete_driver = mutations.DeleteDriverType.Field()
    create_geofence = mutations.CreateGeofenceType.Field()
    update_geofence = mutations.UpdateGeofenceType.Field()
    delete_geofence = mutations.DeleteGeofenceType.Field()
    create_calendar = mutations.CreateCalendarType.Field()
    update_calendar = mutations.UpdateCalendarType.Field()
    delete_calendar = mutations.DeleteCalendarType.Field()
    enable_web_notification = mutations.EnableWebNotificationType.Field()
    disable_web_notification = mutations.DisableWebNotificationType.Field()
    enable_email_notification = mutations.EnableEmailNotificationType.Field()
    disable_email_notification = mutations.DisableEmailNotificationType.Field()
    enable_sms_notification = mutations.EnableSmsNotificationType.Field()
    disable_sms_notification = mutations.DisableSmsNotificationType.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
