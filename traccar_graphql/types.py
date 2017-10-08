import datetime, iso8601
from graphene.types import datetime
from graphql.language import ast

class DateTime(datetime.DateTime):
    '''Graphene DateTime overide'''

    @staticmethod
    def serialize(dt):
        if isinstance(dt, str):
            dt = iso8601.parse_date(dt)
        return datetime.DateTime.serialize(dt)
