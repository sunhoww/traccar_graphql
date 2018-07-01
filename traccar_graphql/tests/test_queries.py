from graphene.test import Client

from traccar_graphql.schema import schema


def test_query_server(snapshot):
    """Testing query for server"""
    client = Client(schema)
    snapshot.assert_match(client.execute('''{ server {
        id
        map
        latitude
        longitude
        zoom
        readonly
        deviceReadonly
        distanceUnit
        speedUnit
        timezone
        twelveHourFormat
        coordinateFormat
        version
        mapUrl
        registration
        forceSettings
        bingKey
        limitCommands
        } }'''))


def test_query_me(snapshot):
    """Testing query for me"""
    client = Client(schema)
    snapshot.assert_match(client.execute('''{ me {
        id
        map
        latitude
        longitude
        zoom
        readonly
        deviceReadonly
        distanceUnit
        speedUnit
        timezone
        twelveHourFormat
        coordinateFormat
        email
        name
        phone
        password
        admin
        disabled
        userLimit
        deviceLimit
        expirationTime
        token
        } }'''))
