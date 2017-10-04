import os, graphene, requests

from traccar_graphql.models import ServerType
from traccar_graphql.utils import request2object

TRACCAR_BACKEND = os.environ.get('TRACCAR_BACKEND')

class Query(graphene.ObjectType):
    server = graphene.Field(lambda: ServerType)
    def resolve_server(self, args, context, info):
        r = requests.get("{}/api/server".format(TRACCAR_BACKEND))
        return request2object(r, 'ServerType')

schema=graphene.Schema(query=Query)
