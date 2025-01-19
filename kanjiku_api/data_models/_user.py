import datetime

from tortoise import fields
from tortoise.models import Model


class User(Model):
    """Model Representing a User

    Attributes:
        username (str): Name of the User.
        password_hash (str, optional): Passwordhash for local Users
        auth_type (AuthSource): How to authenticate the User.
        email (str): Email address of the User.
        activated (bool): User verified his email Address.
    """

    username: str = fields.CharField(
        max_length=30, unique=True, pk=True, description="Username"
    )
    password_hash: bytes = fields.BinaryField(
        description="Hash of the password (if local user)", null=True
    )
    email: str = fields.CharField(
        max_length=100,
        unique=True,
        description="Email address for the user",
    )
    activated: bool = fields.BooleanField(
        description="0: User did not verify his Email\n1: User verified his Email",
        default=False
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
    refresh_tokens: fields.ReverseRelation["RefreshToken"]
    identity_tokens: fields.ReverseRelation["IdentityToken"]
    read_chapters = fields.ManyToManyField(
        model_name="data_models.Chapter",
        through="read_chapters",
        related_name="read_by",
    )
    read_chapters = fields.ManyToManyField(
        model_name="data_models.Announcement",
        through="read_announcements",
        related_name="read_by",
    )
