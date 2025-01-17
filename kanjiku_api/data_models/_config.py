from tortoise import fields
from tortoise.models import Model

from kanjiku_api.Enums import SettingKey

class Config(Model):
    id = fields.BigIntField(primary_key=True)
    option:SettingKey = fields.CharEnumField(SettingKey)