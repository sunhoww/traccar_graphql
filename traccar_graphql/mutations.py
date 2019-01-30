import graphene
from graphene import relay
from graphql import GraphQLError
from flask_jwt_extended import create_access_token, create_refresh_token

from traccar_graphql import models, api
from traccar_graphql.utils import dict2object


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

    access_token = graphene.String()
    refresh_token = graphene.String()
    user = graphene.Field(models.User)

    @classmethod
    def mutate_and_get_payload(cls, root, info, email, password):
        r = api.call(
            "session",
            method="POST",
            auth=False,
            data={"email": email, "password": password},
        )
        if r.status_code == 401:
            raise GraphQLError("Invalid credentials")
        data = r.json()
        identity = _Indentity(
            id=data["id"],
            email=data["email"],
            admin=data["administrator"],
            session=r.headers["Set-Cookie"],
        )
        return Login(
            access_token=create_access_token(identity=identity),
            refresh_token=create_refresh_token(identity=identity),
            user=dict2object(data, models.UserType),
        )
