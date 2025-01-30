import re
import datetime

from uuid import UUID
from typing import Optional

from tortoise import fields
from tortoise.models import Model
from tortoise.validators import MinLengthValidator, RegexValidator


class User(Model):
    """Model Representing a User

    Attributes:
        username (str): Name of the User.
        password_hash (str, optional): Passwordhash for local Users
        auth_type (AuthSource): How to authenticate the User.
        email (str): Email address of the User.
        activated (bool): User verified his email Address.
    """

    uuid: UUID = fields.UUIDField(pk=True)
    username: str = fields.CharField(
        max_length=30,
        unique=True,
        description="Username",
        validators=[
            MinLengthValidator(5),
            RegexValidator(
                r"[a-z0-9]+[a-z \._-]+[a-z0-9]",
                re.I,
            ),
        ],
    )
    password_hash: bytes = fields.BinaryField(
        description="Hash of the password", null=True
    )
    email: str = fields.CharField(
        max_length=320,
        unique=True,
        description="Email address for the user",
        validators=[
            RegexValidator(
                r"""^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$""",
                re.I,
            )
        ],
    )
    birthday: Optional[datetime.date] = fields.DateField(null=True)
    activated: bool = fields.BooleanField(
        description="0: User did not verify his Email\n1: User verified his Email",
        default=False,
    )
    created_at: datetime.datetime = fields.DatetimeField(
        auto_now_add=True,
        allows_generated=True,
        GENERATED_SQL="NOW()",
        description="When was this User added to the Database",
    )
    modified_at: datetime.datetime = fields.DatetimeField(
        auto_now=True,
        allows_generated=True,
        GENERATED_SQL="NOW()",
        description="When was the user modified",
    )
    groups = fields.ManyToManyField(
        model_name="data_models.Group",
        through="usergroup",
        related_name="users",
        forward_key="username",
        backward_key="name",
    )
    avatar = fields.ForeignKeyField(model_name="data_models.Image", null=True)

    reset_tokens: fields.ReverseRelation["ResetToken"]
    identity_tokens: fields.ReverseRelation["IdentityToken"]
    read_chapters = fields.ManyToManyField(
        model_name="data_models.Chapter",
        through="read_chapters",
        related_name="read_by",
    )
    read_announcements = fields.ManyToManyField(
        model_name="data_models.Announcement",
        through="read_announcements",
        related_name="read_by",
    )

    @property
    def member_since(self):
        return self.created_at.strftime("%d/%m/%Y")

    async def serialize(self, include_expensive:bool=False, *fields) -> dict:
        birthday = self.birthday
        if birthday is not None:
            birthday = birthday.strftime("%d/%m/%Y")

        avatar = await self.avatar
        if avatar is not None:
            return str(avatar.uuid)

        raw_dict = {
            "id": str(self.uuid),
            "username": self.username,
            "email": self.email,
            "birthday": birthday,
            "activated": self.activated,
            "member_since": self.member_since,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
        }

        if include_expensive:
            raw_dict["read_chapters"] = await self.read_announcements.all().values_list("id", flat=True)
            raw_dict["read_announcements"] = await self.read_announcements.all().values_list("id", flat=True)

        
        return_dict = {}
        raw_dict_keys = raw_dict.keys()
        if len(fields) == 0:
            return raw_dict
        for key in fields:
            if not key in raw_dict_keys:
                continue
            return_dict[key] = raw_dict[key]

        return return_dict