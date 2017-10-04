from flask import Flask
from flask_graphql import GraphQLView

from traccar_graphql.schema import schema

__version__ = '0.0.1'

view_func = GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
)

app = Flask(__name__)
app.add_url_rule('/graphql', view_func=view_func)

if __name__ == '__main__':
    app.run()
