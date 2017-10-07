import os, requests
from promise import Promise
from promise.dataloader import DataLoader
from flask_jwt_extended import get_jwt_claims
from graphql import GraphQLError

from traccar_graphql.utils import request2object, header_with_auth

TRACCAR_BACKEND = os.environ.get('TRACCAR_BACKEND')

def _batch_array(endpoint='', cls_name='GenericType'):
    def fn(self, keys):
        r = requests.get(
            "{}/api/{}".format(TRACCAR_BACKEND, endpoint),
            headers=header_with_auth())
        entities = [next((x for x in request2object(r, cls_name) if x.id == key), None) for key in keys]
        return Promise.resolve(entities)
    return fn

class GroupLoader(DataLoader):
    batch_load_fn = _batch_array(endpoint='groups', cls_name='GroupType')
group_loader = GroupLoader()

class DriverLoader(DataLoader):
    batch_load_fn = _batch_array(endpoint='drivers', cls_name='DriverType')
driver_loader = DriverLoader()

class GeofenceLoader(DataLoader):
    batch_load_fn = _batch_array(endpoint='geofences', cls_name='GeofenceType')
geofence_loader = GeofenceLoader()

class CalendarLoader(DataLoader):
    batch_load_fn = _batch_array(endpoint='calendars', cls_name='CalendarType')
calendar_loader = CalendarLoader()
