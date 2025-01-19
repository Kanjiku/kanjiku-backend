from tortoise import fields
from tortoise.models import Model


class Page(Model):
    id = fields.BigIntField(pk=True)
    page = fields.IntField()
    chapter = fields.ForeignKeyField(model_name="data_models.Chapter", related_name="pages")
    pages: fields.ReverseRelation["Page"]
