import os
from flask import Flask, jsonify
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager, jwt_optional
from graphql import GraphQLError

from traccar_graphql.schema import schema
from traccar_graphql.utils import get_blacklisted_tokens

__version__ = '0.0.1'

app = Flask(__name__)

app.secret_key = os.environ.get('JWT_SECRET')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

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

@jwt.expired_token_loader
def handle_expired_token_error():
    return jsonify({ 'errors': [{ 'message': "Token has expired" }] })

@jwt.invalid_token_loader
def handle_invalid_token_error(msg):
    return jsonify({ 'errors': [{ 'message': msg }] })

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in get_blacklisted_tokens()

view_func = GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
)

app.add_url_rule('/graphql', view_func=jwt_optional(view_func))

if __name__ == '__main__':
    app.run()
