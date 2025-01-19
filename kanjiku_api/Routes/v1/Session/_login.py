import i18n

from sanic import Request
from sanic.response import json as json_resp

from kanjiku_api.data_models import User, RefreshToken, IdentityToken
from kanjiku_api.Exceptions import LoginError
from . import session_bp


@session_bp.route("/login", ["POST"])
async def login(request: Request):
    cfg = request.app.config.CFG
    print(cfg)
    request_data = request.json
    username = request_data.get("username", None)
    email = request_data.get("email", None)
    password = request_data.get("password", None)
    if username is None and email is None:
        raise LoginError(
            {
                "msg": i18n.t("errors.username_or_email_not_provided"),
                "msg_key": "errors.username_or_email_not_provided",
            },
            status_code=400,
        )
    if password is None:
        raise LoginError(
            {
                "msg": i18n.t("errors.password_not_providied"),
                "msg_key": "errors.password_not_providied",
            },
            status_code=400,
        )

    return json_resp({"greeting": i18n.t("errors.hello_world")})
