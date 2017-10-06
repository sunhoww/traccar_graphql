import os
from flask import Flask
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager, jwt_optional

from traccar_graphql.schema import schema

__version__ = '0.0.1'

app = Flask(__name__)

app.secret_key = os.environ.get('JWT_SECRET')

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'id': identity.id,
        'admin': identity.admin,
        'session': identity.session,
    }

@jwt.user_identity_loader
def make_identity_for_access_token(identity):
    return identity.email

view_func = GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
)

app.add_url_rule('/graphql', view_func=jwt_optional(view_func))

if __name__ == '__main__':
    app.run()
