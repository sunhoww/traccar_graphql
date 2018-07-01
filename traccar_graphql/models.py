from graphene import (
    Interface, ObjectType, String, Boolean, Int, Float, Field, List)

from traccar_graphql.types import DateTime
from traccar_graphql.loaders import (
    device_loader, group_loader, user_loader, geofence_loader, position_loader)


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


class GroupType(ObjectType):
    id = Int()
    name = String()
    parent_group = Field(lambda: GroupType)

    def resolve_parent_group(self, args, context, info):
        return group_loader.load(self.group_id)


class DriverType(ObjectType):
    id = Int()
    name = String()
    unique_id = String()


class GeofenceType(ObjectType):
    id = Int()
    name = String()
    description = String()
    area = String()
    calendar = Int()

    def resolve_calendar(self, args, context, info):
        return self.calendar_id


class CalendarType(ObjectType):
    id = Int()
    name = String()
    data = String()


class NotificationTypeType(ObjectType):
    id = Int()
    type = String()


class NotificationType(ObjectType):
    id = Int()
    type = String()
    user = Field(lambda: UserType)
    web = Boolean()
    mail = Boolean()
    sms = Boolean()

    def resolve_user(self, args, context, info):
        return user_loader.load(self.user_id)


class DeviceType(ObjectType):
    id = Int()
    name = String()
    unique_id = String()
    status = String()
    last_update = Field(lambda: DateTime)
    position = Field(lambda: PositionType)
    group = Field(lambda: GroupType)
    phone = String()
    model = String()
    contact = String()
    category = String()
    geofences = List(lambda: GeofenceType)

    def resolve_position(self, args, context, info):
        return position_loader.load(self.position_id)

    def resolve_group(self, args, context, info):
        return group_loader.load(self.group_id)

    def resolve_geofences(self, args, context, info):
        return geofence_loader.load_many(self.geofence_ids)


class PositionType(ObjectType):
    id = Int()
    device = Field(lambda: DeviceType)
    protocol = String()
    device_time = DateTime()
    fix_time = DateTime()
    server_time = String()
    outdated = Boolean()
    valid = Boolean()
    latitude = Float()
    longitude = Float()
    altitude = Float()
    speed = Float(description="in knots")
    course = Float()
    address = String()
    accuracy = Float()
    network = String()

    def resolve_device(self, args, context, info):
        return device_loader('id').load(self.device_id)
