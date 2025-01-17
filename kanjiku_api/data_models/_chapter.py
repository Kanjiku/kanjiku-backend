from datetime import datetime
from tortoise import fields
from tortoise.models import Model


class Chapter(Model):
    id = fields.BigIntField(pk=True)
    number = fields.TextField()
    volume = fields.TextField(null=True)
    name = fields.TextField()
    release_date = fields.DatetimeField(default=datetime.now())
    read_by: fields.ManyToManyRelation["User"]
