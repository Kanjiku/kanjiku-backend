from tortoise import fields
from tortoise.models import Model

class Page(Model):
    id = fields.BigIntField(pk=True)
    name = fields.TextField(unique=True)
    slug = fields.TextField(unique=True)
    description = fields.TextField(null=True)