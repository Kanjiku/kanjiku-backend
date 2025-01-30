from tortoise import fields
from tortoise.models import Model


class RefreshToken(Model):
    uuid = fields.UUIDField(pk=True)
    issued = fields.DatetimeField(auto_now=True)
    valid_until = fields.DatetimeField()
    id_token = fields.ForeignKeyField("data_models.IdentityToken", "refresh_token")
