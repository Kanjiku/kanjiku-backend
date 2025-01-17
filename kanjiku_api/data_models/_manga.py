from tortoise import fields
from tortoise.models import Model


class Manga(Model):
    id = fields.BigIntField(pk=True)
    name = fields.TextField(unique=True)
    slug = fields.TextField(unique=True)
    description = fields.TextField(null=True)
    thumbnail = fields.ForeignKeyField("data_models.Image", related_name="relations")
