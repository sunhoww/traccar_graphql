import aniso8601
from graphene.types import datetime


class DateTime(datetime.DateTime):
    '''Graphene DateTime overide'''

    @staticmethod
    def serialize(dt):
        if isinstance(dt, str):
            dt = aniso8601.parse_date(dt)
        return datetime.DateTime.serialize(dt)
