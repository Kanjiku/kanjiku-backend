import i18n

from sanic import Request
from sanic.response import json as json_resp

from kanjiku_api.data_models import User
from kanjiku_api.Exceptions import UserDoesNotExist
from . import user_bp


@user_bp.route("/", ["GET"])
async def show_user(request: Request):
    return json_resp({"greeting": i18n.t("errors.hello_world")})


@user_bp.route("/<user_id:int>", ["GET"])
async def show_user_by_id(request: Request, user_id: int):
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise UserDoesNotExist(
            {
                "msg": i18n.t("errors.user_does_not_exist").format(id=user_id),
                "msg_key": "errors.user_does_not_exist",
            },
            status_code=404,
        )

    avatar = await user.avatar
    if avatar is not None:
        avatar = avatar.uuid

    groups = await user.groups.all().values_list("name", flat=True)

    repsonse_data = {
        "id": user.id,
        "username": user.username,
        "avatar": avatar,
        "groups": groups,
        "member_since": user.created_at.strftime("%d/%m/%Y")
    }

    if False:
        birthday = user.birthday
        if birthday is not None:
            birthday = birthday.isoformat()
        repsonse_data["birthday"] = birthday
        repsonse_data["email"] = user.email

    return json_resp(repsonse_data)
