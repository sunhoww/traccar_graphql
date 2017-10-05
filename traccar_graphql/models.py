import os, requests
from graphene import Interface, ObjectType, Mutation, String, Boolean, Int, Float, Field
from graphene.types.datetime import DateTime
from graphql import GraphQLError
from flask_jwt_extended import create_access_token

from traccar_graphql.utils import request2object

TRACCAR_BACKEND = os.environ.get('TRACCAR_BACKEND')

class SettingsType(Interface):
    readonly = Boolean()
    device_readonly = Boolean()
    map = Boolean()
    latitude = Float()
    longitude = Float()
    zoom = Int()
    twelve_hour_format = Boolean()
    coordinate_format = String()
    limit_commands = Boolean()

class ServerType(ObjectType):
    class Meta:
        interfaces = (SettingsType, )
    version = String()
    registration = Boolean()
    bing_key = String()
    map_url = String()
    force_settings = Boolean()

class UserType(ObjectType):
    class Meta:
        interfaces = (SettingsType, )
    name = String()
    email = String()
    phone = String()
    admin = Boolean()
    disabled = Boolean()
    expiration_time = DateTime()
    device_limit = Int()
    user_limit = Int()

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
        access_token = create_access_token(identity=identity)
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
