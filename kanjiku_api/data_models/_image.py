from uuid import UUID
from tortoise import fields
from tortoise.models import Model

class Image(Model):
    uuid:UUID = fields.UUIDField(primary_key=True)
    filename = fields.TextField()
    restricted = fields.BooleanField(default=False)
    user_relation: fields.OneToOneRelation["User"]
    manga_relation: fields.OneToOneRelation["Manga"]
    blog_relation: fields.OneToOneRelation["BlogEntry"]