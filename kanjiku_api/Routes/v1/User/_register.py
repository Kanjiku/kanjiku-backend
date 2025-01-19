import i18n

from sanic import Request
from sanic.response import json as json_resp
from sanic.exceptions import SanicException

from kanjiku_api.data_models import User
from . import user_bp


@user_bp.route("/register", ["POST"])
async def register(request: Request):

    request_body = request.json

    if await User.get_or_none(username=request_body["username"]) is not None:
        raise SanicException(
            {
                "msg": i18n.t("errors.username_taken").format(
                    username=request_body["username"]
                ),
                "msg_key": "errors.username_taken",
            }
        )

    user = await User.create(
        username=request_body["username"],
        password_hash=b"deadbeef",
        email="test@test.de",
    )

    return json_resp(
        {
            "msg": i18n.t("messages.user_created").format(
                username=request_body["username"]
            ),
            "msg_key": "messages.user_created",
        }
    )
