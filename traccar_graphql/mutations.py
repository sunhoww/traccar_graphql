import os, requests, datetime
from graphene import Mutation, String, Field
from graphql import GraphQLError
from flask_jwt_extended import create_access_token

from traccar_graphql.models import UserType
from traccar_graphql.utils import request2object

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
            session=r.headers['Set-Cookie']
        )

        # TODO: remove expires_delta
        access_token = create_access_token(identity=identity, expires_delta=datetime.timedelta(days=7))
        return LoginType(access_token=access_token)

class RegisterType(Mutation):
    class Input:
        email = String(description="Used to sign in", required=True)
        name = String()
        password = String(required=True)

    user = Field(lambda: UserType)

    def mutate(self, input, context, info):
        r = requests.post("{}/api/users".format(TRACCAR_BACKEND), json=input)
        if ("Unique index or primary key violation" in r.text):
            raise GraphQLError('User with this email exists')
        return RegisterType(user=request2object(r, 'UserType'))
