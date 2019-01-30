import os

import logging
from flask import Flask, jsonify
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager, jwt_optional

from traccar_graphql.schema import schema
from traccar_graphql.utils import get_blacklisted_tokens

VERSION = "0.0.1"
logger = logging.getLogger(__name__)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("JWT_SECRET", "dev"),
        TRACCAR_BACKEND=os.environ.get("TRACCAR_BACKEND"),
        JWT_BLACKLIST_ENABLED=True,
        JWT_BLACKLIST_TOKEN_CHECKS=["access", "refresh"],
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(identity):
        return {"id": identity.id, "admin": identity.admin, "session": identity.session}

    @jwt.user_identity_loader
    def make_identity_for_access_token(identity):
        return identity.email

    @jwt.expired_token_loader
    def handle_expired_token_error():
        return jsonify({"errors": [{"message": "Token has expired"}]})

    @jwt.invalid_token_loader
    def handle_invalid_token_error(msg):
        return jsonify({"errors": [{"message": msg}]})

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token["jti"]
        return jti in get_blacklisted_tokens()

    @app.after_request
    def cors(response):
        if os.environ.get("FLASK_ENV") == "development":
            response.headers["Access-Control-Allow-Origin"] = os.environ.get(
                "DEVELOPMENT_FRONTEND", "null"
            )
            response.headers["Access-Control-Allow-Headers"] = "content-type"
        return response

    view_func = GraphQLView.as_view("graphql", schema=schema, graphiql=True)
    app.add_url_rule("/", view_func=jwt_optional(view_func))

    return app
