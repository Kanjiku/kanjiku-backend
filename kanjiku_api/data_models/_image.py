from tortoise import fields
from tortoise.models import Model


class Image(Model):
    id = fields.BigIntField(primary_key=True)
    restrcited = fields.BooleanField(default=False)
    filepath = fields.TextField()
    relations: fields.ForeignKeyRelation["User" | "Manga" | "BlogEntry"]