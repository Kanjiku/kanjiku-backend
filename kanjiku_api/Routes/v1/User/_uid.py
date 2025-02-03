import i18n

from uuid import UUID
from sanic import Request
from sanic.response import json as json_resp

from kanjiku_api.data_models import User
from kanjiku_api.Exceptions import UserDoesNotExist
from . import user_bp


@user_bp.route("/<user_id:uuid>", ["GET"])
async def show_user_by_id(request: Request, user_id: UUID):
    user = await User.get_or_none(uuid=user_id)
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
        "uuid": str(user.uuid),
        "username": user.username,
        "avatar": avatar,
        "groups": groups,
        "member_since": user.created_at.strftime("%d/%m/%Y"),
    }

    # if the viewing user is not logged in or
    # not the requesting user or not an admin
    # we return the "sparse" response
    if (
        request.ctx.user_info is None
        or request.ctx.user_info.get("uid", "") != str(user_id)
        or not request.ctx.user_info.get("permissions", {}).get("admin", False)
    ):
        return json_resp(repsonse_data)

    birthday = user.birthday
    if birthday is not None:
        birthday = birthday.isoformat()
    repsonse_data["birthday"] = birthday
    repsonse_data["email"] = user.email

    # if the user is an admin we respond with the session token infos as well
    if request.ctx.user_info.get("permissions", {}).get("admin", False):
        repsonse_data["identity_tokens"] = await user.identity_tokens.all().values_list(
            "uuid", flat=True
        )

    return json_resp(repsonse_data)
