from tortoise import fields
from tortoise.models import Model


class Manga(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    slug = fields.CharField(max_length=255, unique=True)
    description = fields.TextField(null=True)
    thumbnail = fields.ForeignKeyField(
        "data_models.Image", related_name="manga", null=True
    )
