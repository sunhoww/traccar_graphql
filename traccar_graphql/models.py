from graphene import Interface, ObjectType, String, Boolean, Int, Float, Field
from graphene.types.datetime import DateTime

class SettingsType(Interface):
    id = Int()
    map = Boolean()
    latitude = Float()
    longitude = Float()
    zoom = Int()
    readonly = Boolean()
    device_readonly = Boolean()
    distance_unit = String()
    speed_unit = String()
    timezone = String()
    twelve_hour_format = Boolean()
    coordinate_format = String()

class ServerType(ObjectType):
    class Meta:
        interfaces = (SettingsType, )

    version = String()
    map_url = String()
    registration = Boolean()
    force_settings = Boolean()
    bing_key = String()
    limit_commands = Boolean()

class UserType(ObjectType):
    class Meta:
        interfaces = (SettingsType, )

    email = String()
    name = String()
    phone = String()
    password = String()
    admin = Boolean()
    disabled = Boolean()
    user_limit = Int()
    device_limit = Int()
    expiration_time = DateTime()
    token = String()
