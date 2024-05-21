from tortoise import fields
from tortoise.models import Model

class ReadChapter(Model):
    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyRelation("data_models.User", "read_chapters")