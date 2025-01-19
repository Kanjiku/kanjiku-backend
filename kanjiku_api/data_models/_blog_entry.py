from typing import Optional
from tortoise import fields
from tortoise.models import Model


class BlogEntry(Model):
    id = fields.BigIntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)
    text = fields.TextField()
    image: Optional[fields.ForeignKeyField] = fields.ForeignKeyField(
        "data_models.Image", "blog_relation", null=True
    )
