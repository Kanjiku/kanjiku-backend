import i18n
import bcrypt

from sanic import Request
from sanic.response import json as json_resp
from tortoise.exceptions import ValidationError

from kanjiku_api.data_models import User
from kanjiku_api.Exceptions import LoginError
from kanjiku_api.Utility import JWTHelper
from . import session_bp


@session_bp.route("/login", ["POST"])
async def login(request: Request):
    request_data = request.json
    username = request_data.get("username", None)
    password = request_data.get("password", None)
    if username is None:
        raise LoginError(
            {
                "msg": i18n.t("errors.login_not_provided"),
                "msg_key": "errors.login_not_provided",
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

    if "@" in username:
        login_data = {"email": username}
    else:
        login_data = {"username": username}

    user = None
    try:
        user = await User.get_or_none(**login_data)
    except ValidationError:
        # this will get thrown if the username is to short
        raise LoginError(
            {
                "msg": i18n.t("errors.email_invalid"),
                "msg_key": "errors.email_invalid",
            },
            status_code=400,
        )
    if user is None:
        raise LoginError(
            {
                "msg": i18n.t("errors.login_no_user").format(username=username),
                "msg_key": "errors.login_no_user",
            },
            status_code=400,
        )

    if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
        raise LoginError(
            {
                "msg": i18n.t("errors.login_wrong_password").format(username=username),
                "msg_key": "errors.login_wrong_password",
            },
            status_code=400,
        )

    jwt_helper:JWTHelper = request.app.ctx.jwt
    identity, id_token = await jwt_helper.create_id_token(user)
    refresh_token = await jwt_helper.create_refresh_token(identity)

    return json_resp({"id_token": id_token, "refresh_token": refresh_token})
