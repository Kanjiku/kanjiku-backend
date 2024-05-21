from tortoise import fields
from tortoise.models import Model


class Announcement(Model):
    id = fields.BigIntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)
    text = fields.TextField()
