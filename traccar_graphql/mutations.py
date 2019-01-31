import graphene
from graphene import relay
from graphql import GraphQLError
from flask_jwt_extended import create_access_token, get_raw_jwt

from traccar_graphql import api, exceptions
from traccar_graphql.models import user
from traccar_graphql.utils import dict2object, blacklist_token


class _Indentity:
    def __init__(self, id, email=None, admin=False, session=None):
        self.id = id
        self.email = email
        self.admin = admin
        self.session = session


class Login(relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    me = graphene.Field(user.User)

    @classmethod
    def mutate_and_get_payload(cls, root, info, email, password):
        r = api.call(
            "session",
            method="POST",
            auth=False,
            data={"email": email, "password": password},
        )
        if r.status_code == 401:
            raise GraphQLError(exceptions.INVALID_CREDENTIALS)
        data = r.json()
        identity = _Indentity(
            id=data["id"],
            email=data["email"],
            admin=data["administrator"],
            session=r.headers["Set-Cookie"],
        )
        access_token = create_access_token(identity=identity)

        # this sets the token in the request object. Used by GraphQLViewWithCookie
        setattr(info.context, "jwt_access_token", access_token)
        return Login(me=dict2object(data, user.User))


class Logout(relay.ClientIDMutation):
    @classmethod
    def mutate_and_get_payload(cls, root, info):
        api.call("session", method="DELETE")
        blacklist_token(get_raw_jwt()["jti"])
        return Logout()
