import jwt
import datetime

from uuid import UUID
from jwt.exceptions import InvalidTokenError
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

    async def _token_info(self, user: User) -> tuple[dict[str, bool], list[str]]:

        groups: list[Group] = await user.groups.all()
        group_names: list[str] = [group.name for group in groups]

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

        return permissions, group_names

    async def create_id_token(self, user: User):

        valid_until = datetime.datetime.now() + datetime.timedelta(
            minutes=self.valid_minutes_id
        )
        id_token = await IdentityToken.create(user=user, valid_until=valid_until)

        jwt_header = {"kid": str(id_token.id), "token": "IdentityToken"}

        permissions, group_names = await self._token_info(user)

        jwt_data = {
            "iss": self.issuer,
            "iat": datetime.datetime.now().timestamp(),
            "nbf": datetime.datetime.now().timestamp(),
            "exp": valid_until.timestamp(),
            "user": {
                "uid": str(user.id),
                "username": user.username,
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
        refresh_token = await RefreshToken.create(
            valid_until=valid_until, id_token=id_token
        )

        jwt_header = {"kid": str(refresh_token.id), "token": "RefreshToken"}

        jwt_data = {
            "iss": self.issuer,
            "iat": datetime.datetime.now().timestamp(),
            "nbf": datetime.datetime.now().timestamp(),
            "exp": valid_until.timestamp(),
            "id_token": str(id_token.id),
        }

        token = jwt.encode(
            jwt_data,
            self.secret,
            headers=jwt_header,
            algorithm=self.signmethod.value,
        )

        return token

    async def renew_tokens(self, refresh_token: str) -> tuple[ſtr, str]:
        # validate jwt
        jwt_data = jwt.decode(refresh_token, self.secret, self.signmethod.value)

        id_token_id = jwt_data.get("id_token", None)
        # check if the token has a id_token id given
        if id_token_id is None:
            raise InvalidTokenError()

        # check if the header has a refresh token id given
        refresh_token_id = jwt.get_unverified_header(refresh_token).get("kid", None)
        if refresh_token_id is None:
            raise InvalidTokenError()

        # try to get refresh_token via id
        try:
            refresh_token_obj = await RefreshToken.get_or_none(
                id=UUID(refresh_token_id)
            )
        except ValueError:
            # if the UUID is invalid
            raise InvalidTokenError()

        if refresh_token_obj is None:
            raise InvalidTokenError()

        # try to get id_token via id
        try:
            id_token = await IdentityToken.get_or_none(id=UUID(id_token_id))
        except ValueError:
            # if the UUID is invalid
            raise InvalidTokenError()

        if id_token is None:
            # no id token with given id... not gonna create a new one
            raise InvalidTokenError()

        valid_until = datetime.datetime.now() + datetime.timedelta(
            minutes=self.valid_minutes_id
        )

        id_token.valid_until = valid_until
        await id_token.save()

        jwt_header = {"kid": str(id_token.id), "token": "IdentityToken"}
        jwt_data = {
            "iss": self.issuer,
            "iat": datetime.datetime.now().timestamp(),
            "nbf": datetime.datetime.now().timestamp(),
            "exp": valid_until.timestamp(),
            "id_token": str(id_token.id),
        }

        updated_id_token = jwt.encode(
            jwt_data,
            self.secret,
            headers=jwt_header,
            algorithm=self.signmethod.value,
        )

        valid_until = datetime.datetime.now() + datetime.timedelta(
            minutes=self.valid_minutes_refresh
        )
        refresh_token_obj.valid_until = valid_until
        await refresh_token_obj.save()

        jwt_header = {"kid": str(refresh_token_obj.id), "token": "RefreshToken"}

        jwt_data = {
            "iss": self.issuer,
            "iat": datetime.datetime.now().timestamp(),
            "nbf": datetime.datetime.now().timestamp(),
            "exp": valid_until.timestamp(),
            "id_token": str(id_token.id),
        }

        updated_refresh_token = jwt.encode(
            jwt_data,
            self.secret,
            headers=jwt_header,
            algorithm=self.signmethod.value,
        )

        return updated_id_token, updated_refresh_token
