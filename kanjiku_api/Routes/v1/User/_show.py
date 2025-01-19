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
            }, status_code=404
        )
    
    return json_resp({"id":user.id})
