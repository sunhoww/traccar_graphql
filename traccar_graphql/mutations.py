import os, requests, datetime
from graphene import Mutation, InputObjectType, String, Field, Int, Argument
from graphql import GraphQLError
from flask_jwt_extended import get_raw_jwt

from traccar_graphql import models
from traccar_graphql.utils import request2object, camelify_keys, blacklist_token, header_with_auth

TRACCAR_BACKEND = os.environ.get('TRACCAR_BACKEND')

class _Indentity():
    def __init__(self, id, email=None, admin=False, session=None):
        self.id = id
        self.email = email
        self.admin = admin
        self.session = session

class LoginType(Mutation):
    class Input:
        email = String(required=True)
        password = String(required=True)

    access_token = String()

    def mutate(self, input, context, info):
        email = input.get('email')
        password = input.get('password')
        r = requests.post("{}/api/session".format(TRACCAR_BACKEND), data=input)
        if (r.status_code == 401):
            raise GraphQLError('Invalid credentials')
        data = r.json()
        identity = _Indentity(
            id=data['id'],
            email=data['email'],
            admin=data['admin'],
            session=r.headers['Set-Cookie'])

        # TODO: remove expires_delta
        access_token = create_access_token(identity=identity, expires_delta=datetime.timedelta(days=7))
        return LoginType(access_token=access_token)

class LogoutType(Mutation):
    access_token = String()

    def mutate(self, input, context, info):
        r = requests.delete("{}/api/session".format(TRACCAR_BACKEND), headers=header_with_auth())
        blacklist_token(get_raw_jwt()['jti'])
        return LogoutType(access_token=None)

class RegisterType(Mutation):
    class Input:
        email = String(description="Used to sign in", required=True)
        name = String()
        password = String(required=True)

    user = Field(lambda: models.UserType)

    def mutate(self, input, context, info):
        r = requests.post("{}/api/users".format(TRACCAR_BACKEND), json=input)
        if ("Unique index or primary key violation" in r.text):
            raise GraphQLError('User with this email exists')
        return RegisterType(user=request2object(r, 'UserType'))


class GroupInput(InputObjectType):
    name = String()
    group_id = Int()

class CreateGroupType(Mutation):
    class Input:
        input = Argument(lambda: GroupInput)

    group = Field(lambda: models.GroupType)

    def mutate(self, args, context, info):
        r = requests.post(
            "{}/api/groups".format(TRACCAR_BACKEND),
            headers=header_with_auth(),
            json=camelify_keys(args.get('input')))
        return CreateGroupType(group=request2object(r, 'GroupType'))

class UpdateGroupType(Mutation):
    class Input:
        id = Int(required=True)
        input = Argument(lambda: GroupInput)

    group = Field(lambda: models.GroupType)

    def mutate(self, args, context, info):
        patch = camelify_keys(args.get('input'))
        patch['id'] = args.get('id')
        r = requests.put(
            "{}/api/groups/{}".format(TRACCAR_BACKEND, patch['id']),
            headers=header_with_auth(),
            json=patch)
        return UpdateGroupType(group=request2object(r, 'GroupType'))

class DeleteGroupType(Mutation):
    class Input:
        id = Int(required=True)

    id = Int()
    def mutate(self, args, context, info):
        r = requests.delete(
            "{}/api/groups/{}".format(TRACCAR_BACKEND, args.get('id')),
            headers=header_with_auth())
        return DeleteGroupType(id=args.get('id'))

class DriverInput(InputObjectType):
    name = String()
    unique_id = String()

class CreateDriverType(Mutation):
    class Input:
        input = Argument(lambda: DriverInput)

    driver = Field(lambda: models.DriverType)

    def mutate(self, args, context, info):
        r = requests.post(
            "{}/api/drivers".format(TRACCAR_BACKEND),
            headers=header_with_auth(),
            json=camelify_keys(args.get('input')))
        return CreateDriverType(driver=request2object(r, 'DriverType'))

class UpdateDriverType(Mutation):
    class Input:
        id = Int(required=True)
        input = Argument(lambda: DriverInput)

    driver = Field(lambda: models.DriverType)

    def mutate(self, args, context, info):
        patch = camelify_keys(args.get('input'))
        patch['id'] = args.get('id')
        r = requests.put(
            "{}/api/drivers/{}".format(TRACCAR_BACKEND, patch['id']),
            headers=header_with_auth(),
            json=patch)
        return UpdateDriverType(driver=request2object(r, 'DriverType'))

class DeleteDriverType(Mutation):
    class Input:
        id = Int(required=True)

    id = Int()
    def mutate(self, args, context, info):
        r = requests.delete(
            "{}/api/drivers/{}".format(TRACCAR_BACKEND, args.get('id')),
            headers=header_with_auth())
        return DeleteDriverType(id=args.get('id'))

class GeofenceInput(InputObjectType):
    name = String()
    description = String()
    area = String()
    calendar_id = Int()

class CreateGeofenceType(Mutation):
    class Input:
        input = Argument(lambda: GeofenceInput)

    geofence = Field(lambda: models.GeofenceType)

    def mutate(self, args, context, info):
        r = requests.post(
            "{}/api/geofences".format(TRACCAR_BACKEND),
            headers=header_with_auth(),
            json=camelify_keys(args.get('input')))
        return CreateGeofenceType(geofence=request2object(r, 'GeofenceType'))

class UpdateGeofenceType(Mutation):
    class Input:
        id = Int(required=True)
        input = Argument(lambda: GeofenceInput)

    geofence = Field(lambda: models.GeofenceType)

    def mutate(self, args, context, info):
        patch = camelify_keys(args.get('input'))
        patch['id'] = args.get('id')
        r = requests.put(
            "{}/api/geofences/{}".format(TRACCAR_BACKEND, patch['id']),
            headers=header_with_auth(),
            json=patch)
        return UpdateGeofenceType(geofence=request2object(r, 'GeofenceType'))

class DeleteGeofenceType(Mutation):
    class Input:
        id = Int(required=True)

    id = Int()
    def mutate(self, args, context, info):
        r = requests.delete(
            "{}/api/geofences/{}".format(TRACCAR_BACKEND, args.get('id')),
            headers=header_with_auth())
        return DeleteGeofenceType(id=args.get('id'))

class CalendarInput(InputObjectType):
    name = String()
    description = String()
    area = String()
    calendar_id = Int()

class CreateCalendarType(Mutation):
    class Input:
        input = Argument(lambda: CalendarInput)

    calendar = Field(lambda: models.CalendarType)

    def mutate(self, args, context, info):
        r = requests.post(
            "{}/api/calendars".format(TRACCAR_BACKEND),
            headers=header_with_auth(),
            json=camelify_keys(args.get('input')))
        return CreateCalendarType(calendar=request2object(r, 'CalendarType'))

class UpdateCalendarType(Mutation):
    class Input:
        id = Int(required=True)
        input = Argument(lambda: CalendarInput)

    calendar = Field(lambda: models.CalendarType)

    def mutate(self, args, context, info):
        patch = camelify_keys(args.get('input'))
        patch['id'] = args.get('id')
        r = requests.put(
            "{}/api/calendars/{}".format(TRACCAR_BACKEND, patch['id']),
            headers=header_with_auth(),
            json=patch)
        return UpdateCalendarType(calendar=request2object(r, 'CalendarType'))

class DeleteCalendarType(Mutation):
    class Input:
        id = Int(required=True)

    id = Int()
    def mutate(self, args, context, info):
        r = requests.delete(
            "{}/api/calendars/{}".format(TRACCAR_BACKEND, args.get('id')),
            headers=header_with_auth())
        return DeleteCalendarType(id=args.get('id'))

class NotificationInput(InputObjectType):
    type = String()
    user_id = Int()

def _mutate_notification(service, state):
    class holder_class(object):
        def __init__(self, notification):
            self.notification = notification
    def fn(self, args, context, info):
        patch = camelify_keys(args.get('input'))
        patch[service] = state
        r = requests.post(
            "{}/api/users/notifications".format(TRACCAR_BACKEND),
            headers=header_with_auth(),
            json=patch)
        return holder_class(notification=request2object(r, 'NotificationType'))
    return fn

class EnableWebNotificationType(Mutation):
    class Input:
        input = Argument(lambda: NotificationInput)
    notification = Field(lambda: models.NotificationType)
    mutate = _mutate_notification('web', True)

class DisableWebNotificationType(Mutation):
    class Input:
        input = Argument(lambda: NotificationInput)
    notification = Field(lambda: models.NotificationType)
    mutate = _mutate_notification('web', False)

class EnableEmailNotificationType(Mutation):
    class Input:
        input = Argument(lambda: NotificationInput)
    notification = Field(lambda: models.NotificationType)
    mutate = _mutate_notification('mail', True)

class DisableEmailNotificationType(Mutation):
    class Input:
        input = Argument(lambda: NotificationInput)
    notification = Field(lambda: models.NotificationType)
    mutate = _mutate_notification('mail', False)

class EnableSmsNotificationType(Mutation):
    class Input:
        input = Argument(lambda: NotificationInput)
    notification = Field(lambda: models.NotificationType)
    mutate = _mutate_notification('sms', True)

class DisableSmsNotificationType(Mutation):
    class Input:
        input = Argument(lambda: NotificationInput)
    notification = Field(lambda: models.NotificationType)
    mutate = _mutate_notification('sms', False)
