from tortoise import fields
from tortoise.models import Model


class IdentityToken(Model):
    id = fields.BigIntField(pk=True)
    issued = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyRelation("data_models.User", "identity_tokens")
