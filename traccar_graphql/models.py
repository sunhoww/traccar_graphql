import os, requests, datetime
from graphene import Interface, ObjectType, Mutation, String, Boolean, Int, Float, Field
from graphene.types.datetime import DateTime
from graphql import GraphQLError
from flask_jwt_extended import create_access_token

from traccar_graphql.utils import request2object

TRACCAR_BACKEND = os.environ.get('TRACCAR_BACKEND')

class SettingsType(Interface):
    id = Int()
    map = Boolean()
    latitude = Float()
    longitude = Float()
    zoom = Int()
    readonly = Boolean()
    device_readonly = Boolean()
    distance_unit = String()
    speed_unit = String()
    timezone = String()
    twelve_hour_format = Boolean()
    coordinate_format = String()

class ServerType(ObjectType):
    class Meta:
        interfaces = (SettingsType, )

    version = String()
    map_url = String()
    registration = Boolean()
    force_settings = Boolean()
    bing_key = String()
    limit_commands = Boolean()

class UserType(ObjectType):
    class Meta:
        interfaces = (SettingsType, )

    email = String()
    name = String()
    phone = String()
    password = String()
    admin = Boolean()
    disabled = Boolean()
    user_limit = Int()
    device_limit = Int()
    expiration_time = DateTime()
    token = String()

class _Indentity():
    def __init__(self, id, email=None, admin=False, session=None):
        self.id = id
        self.email = email
        self.admin = admin
        self.session = session

class LoginType(Mutation):
    class Input:
        email = String()
        password = String()

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
            session=r.headers['Set-Cookie']
        )

        # TODO: remove expires_delta
        access_token = create_access_token(identity=identity, expires_delta=datetime.timedelta(days=7))
        return LoginType(access_token)

class RegisterType(Mutation):
    class Input:
        email = String(description="Used to sign in")
        name = String()
        password = String()

    user = Field(lambda: UserType)

    def mutate(self, input, context, info):
        r = requests.post("{}/api/users".format(TRACCAR_BACKEND), json=input)
        if ("Unique index or primary key violation" in r.text):
            raise GraphQLError('User with this email exists')
        return RegisterType(user=request2object(r, 'UserType'))
