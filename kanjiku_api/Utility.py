import jwt
import datetime

from dataclasses import dataclass
from kanjiku_api.Enums import SignMethod
from kanjiku_api.data_models import IdentityToken, RefreshToken, User, Group


@dataclass
class JWTHelper:
    issuer: str
    signmethod: SignMethod
    secret: str
    valid_minutes_id: int = 60
    valid_minutes_refresh: int = 1440

    async def create_id_token(self, user: User):

        valid_until = datetime.datetime.now() + datetime.timedelta(
            minutes=self.valid_minutes_id
        )
        id_token = await IdentityToken.create(user=user, valid_until=valid_until)

        groups: list[Group] = await user.groups.all()
        group_names: list[str] = await groups.values_list("name", flat=True)

        permissions = {
            "admin": False,
            "early_access": False,
            "manage_projects": False,
            "upload_chapters": False,
            "moderate_avatars": False,
            "view_hidden": False,
        }

        for group in groups:
            if group.admin:
                permissions["admin"] = True
            if group.early_access:
                permissions["early_access"] = True
            if group.manage_projects:
                permissions["manage_projects"] = True
            if group.upload_chapters:
                permissions["upload_chapters"] = True
            if group.moderate_avatars:
                permissions["moderate_avatars"] = True
            if group.view_hidden:
                permissions["view_hidden"] = True

        jwt_header = {"kid": id_token.id, "token": "IdentityToken"}

        jwt_data = {
            "iss": self.issuer,
            "iat": datetime.datetime.now().timestamp(),
            "nbf": datetime.datetime.now().timestamp(),
            "exp": valid_until.timestamp(),
            "sub": {
                "uid": user.id,
                "user": user.username,
                "groups": group_names,
                "permissions": permissions,
            },
        }

        token = jwt.encode(
            jwt_data,
            self.secret,
            headers=jwt_header,
            algorithm=self.signmethod.value,
        )

        return id_token, token

    async def create_refresh_token(self, id_token: IdentityToken):
        valid_until = datetime.datetime.now() + datetime.timedelta(
            minutes=self.valid_minutes_refresh
        )
        refresh_token = await RefreshToken.create(valid_until=valid_until, id_token=id_token)

        jwt_header = {"kid": refresh_token.id, "token": "RefreshToken"}

        jwt_data = {
            "iss": self.issuer,
            "iat": datetime.datetime.now().timestamp(),
            "nbf": datetime.datetime.now().timestamp(),
            "exp": valid_until.timestamp(),
            "sub": {
                "id": id_token.id,
            },
        }

        token = jwt.encode(
            jwt_data,
            self.secret,
            headers=jwt_header,
            algorithm=self.signmethod.value,
        )

        return token