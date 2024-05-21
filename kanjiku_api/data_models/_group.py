from tortoise import fields
from tortoise.models import Model

from kanjiku_api.data_models._user import User


class Group(Model):
    """Database Model Representing a Group.

    Groups are used for Permission.

    Attributes:
        name (str): Name of the Usergroup.
        users (list[User]): List of Users in this group.
        early_access (int): How many days before Release someone can read Stuff.
        upload_chapters (bool): Can Upload chapters and modify them.
        moderate_avatars (bool): Can delete Avatars for all Users.
        manage_projects (bool): Can create/update/delete Mangas.
        view_hidden (bool): Can view hidden Chapters.
        admin (bool): Full administrative access.
    """

    name: str = fields.CharField(unique=True, max_length=50, pk=True)
    users: fields.ManyToManyRelation[User]
    early_access: int = fields.IntField(default=0)
    upload_chapters = fields.BooleanField(default=False)
    moderate_avatars = fields.BooleanField(default=False)
    manage_projects = fields.BooleanField(default=False)
    view_hidden = fields.BooleanField(default=False)
    admin = fields.BooleanField(default=False)

    def __str__(self):
        return self.name
