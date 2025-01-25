from tortoise import fields
from tortoise.models import Model


class IdentityToken(Model):
    id = fields.UUIDField(pk=True)
    issued = fields.DatetimeField(auto_now=True)
    valid_until = fields.DatetimeField()
    refresh_token: fields.ReverseRelation["RefreshToken"]
    user = fields.ForeignKeyRelation("data_models.User", "identity_tokens")
