from tortoise import fields
from tortoise.models import Model
from typing import Union

class Image(Model):
    uuid = fields.UUIDField(primary_key=True)
    restrcited = fields.BooleanField(default=False)
    filepath = fields.TextField()
    user_relations: fields.OneToOneRelation["User"]
    manga_relations: fields.OneToOneRelation["Manga"]
    blog_relations: fields.OneToOneRelation["BlogEntry"]