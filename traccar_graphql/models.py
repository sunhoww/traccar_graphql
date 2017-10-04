from graphene import ObjectType, String, Boolean, Int, Float

class ServerType(ObjectType):
    version = String()
    registration = Boolean()
    readonly = Boolean()
    device_readonly = Boolean()
    map = Boolean()
    bing_key = String()
    map_url = String()
    latitude = Float()
    longitude = Float()
    zoom = Int()
    twelve_hour_format = Boolean()
    force_settings = Boolean()
    coordinate_format = String()
    limit_commands = Boolean()
