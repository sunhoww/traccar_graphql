import os, requests
from promise import Promise
from promise.dataloader import DataLoader
from flask_jwt_extended import get_jwt_claims
from graphql import GraphQLError

from traccar_graphql.utils import request2object, header_with_auth, current_user_id

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

class NotificationLoader(DataLoader):
    def batch_load_fn(self, keys):
        r = requests.get(
            "{}/api/users/notifications".format(TRACCAR_BACKEND),
            headers=header_with_auth())
        entities = [next((x for x in request2object(r, 'NotificationType') if x.type == key), None) for key in keys]
        return Promise.resolve(entities)
notification_loader = NotificationLoader()

def _fetch_user(user_id):
    url = "{}/api/users".format(TRACCAR_BACKEND)
    params={ 'userId': user_id }
    if user_id == current_user_id():
        url = "{}/api/session".format(TRACCAR_BACKEND)
        params = None
    def fn(resolve, reject):
        try:
            r = requests.get(url, params=params, headers=header_with_auth())
            if r.status_code != 200:
                reject(r.text)
            resolve(request2object(r, 'UserType'))
        except Exception as e:
            reject(e)
    return fn
class UserLoader(DataLoader):
    def batch_load_fn(self, keys):
        entities = [Promise(_fetch_user(key)) for key in keys]
        return Promise.all(entities)
user_loader = UserLoader()
