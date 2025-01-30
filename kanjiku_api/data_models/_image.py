from uuid import UUID
from tortoise import fields
from tortoise.models import Model

class Image(Model):
    uuid:UUID = fields.UUIDField(primary_key=True)
    restrcited = fields.BooleanField(default=False)
    filepath = fields.TextField()
    user_relations: fields.OneToOneRelation["User"]
    manga_relations: fields.OneToOneRelation["Manga"]
    blog_relations: fields.OneToOneRelation["BlogEntry"]