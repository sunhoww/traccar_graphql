import os, requests, datetime
from graphene import Mutation, InputObjectType, String, Field, Int, Argument
from graphql import GraphQLError

from traccar_graphql.models import UserType, GroupType
from traccar_graphql.utils import request2object, camelify_keys, header_with_auth

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


class GroupInput(InputObjectType):
    name = String()
    group_id = Int()

class CreateGroupType(Mutation):
    class Input:
        input = Argument(lambda: GroupInput)

    group = Field(lambda: GroupType)

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

    group = Field(lambda: GroupType)

    def mutate(self, args, context, info):
        patch = args.get('input')
        patch['id'] = args.get('id')
        r = requests.put(
            "{}/api/groups/{}".format(TRACCAR_BACKEND, patch['id']),
            headers=header_with_auth(),
            json=patch)
        return CreateGroupType(group=request2object(r, 'GroupType'))

class DeleteGroupType(Mutation):
    class Input:
        id = Int(required=True)

    id = Int()
    def mutate(self, args, context, info):
        r = requests.delete(
            "{}/api/groups/{}".format(TRACCAR_BACKEND, args.get('id')),
            headers=header_with_auth())
        return DeleteGroupType(id=args.get('id'))
