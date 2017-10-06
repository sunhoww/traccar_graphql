import os, requests
from flask_jwt_extended import get_jwt_claims
from graphql import GraphQLError

from traccar_graphql.utils import request2object

TRACCAR_BACKEND = os.environ.get('TRACCAR_BACKEND')

# TODO: somehow have resolve_groups use DataLoader 

def resolve_groups(self, args, context, info):
    claims = get_jwt_claims()
    if 'session' not in claims:
        raise GraphQLError('Authentication required')
    headers = { 'Cookie': claims['session'] }
    r = requests.get("{}/api/groups".format(TRACCAR_BACKEND), headers=headers)
    return request2object(r, 'GroupType')
