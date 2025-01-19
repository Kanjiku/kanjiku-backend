import i18n

from sanic import Request
from sanic.response import json as json_resp

from kanjiku_api.data_models import User
from kanjiku_api.Exceptions import RegistrationFail
from . import user_bp


@user_bp.route("/register", ["POST"])
async def register(request: Request):

    request_body = request.json

    if await User.get_or_none(username=request_body["username"]) is not None:
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.username_taken").format(
                    username=request_body["username"]
                ),
                "msg_key": "errors.username_taken",
            }
        )

    if await User.get_or_none(email=request_body["email"]) is not None:
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.email_taken").format(
                    email=request_body["email"]
                ),
                "msg_key": "errors.email_taken",
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
