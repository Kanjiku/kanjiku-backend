from tortoise import fields
from tortoise.models import Model
from typing import Union

class Image(Model):
    id = fields.BigIntField(primary_key=True)
    restrcited = fields.BooleanField(default=False)
    filepath = fields.TextField()
    relations: fields.ForeignKeyRelation[Union["User", "Manga", "BlogEntry"]]