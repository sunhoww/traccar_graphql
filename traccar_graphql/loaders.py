import os, requests
from promise import Promise
from promise.dataloader import DataLoader
from flask_jwt_extended import get_jwt_claims
from graphql import GraphQLError

from traccar_graphql.utils import request2object, header_with_auth

TRACCAR_BACKEND = os.environ.get('TRACCAR_BACKEND')

class GroupLoader(DataLoader):
    def batch_load_fn(self, keys):
        r = requests.get(
            "{}/api/groups".format(TRACCAR_BACKEND),
            headers=header_with_auth()
            )
        groups = request2object(r, 'GroupType')
        entities = []
        for key in keys:
            entities.append(next((x for x in groups if x.id == key), None))
        return Promise.resolve(entities)

group_loader = GroupLoader()
