from uuid import UUID
from datetime import datetime
from tortoise import fields
from tortoise.models import Model


class IdentityToken(Model):
    id:UUID = fields.UUIDField(pk=True)
    issued:datetime = fields.DatetimeField(auto_now=True)
    valid_until:datetime = fields.DatetimeField()
    refresh_token: fields.ReverseRelation["RefreshToken"]
    user = fields.ForeignKeyRelation("data_models.User", "identity_tokens")
