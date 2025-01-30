import i18n
from sanic import Blueprint, Request
from sanic.response import json as json_resp
from kanjiku_api.Utility import JWTHelper
from kanjiku_api.Exceptions import SessionError
from kanjiku_api.data_models import IdentityToken

session_bp = Blueprint("Session", "/Session")

from . import _login, _refresh, _logout


@session_bp.route("/", ["GET"])
async def session_info(request: Request):
    jwt_helper: JWTHelper = request.app.ctx.jwt

    identity_token = request.cookies.get("IdentityToken", None)
    refresh_token = request.cookies.get("RefreshToken", None)
    if identity_token is None or refresh_token is None:
        raise SessionError(
            {
                "msg": i18n.t("errors.no_refresh_token_provided"),
                "msg_key": "errors.no_refresh_token_provided",
            },
            status_code=400,
        )

    user_data, _ = jwt_helper.token_data(identity_token)

    return json_resp(
        {
            "id_valid_until": jwt_helper.token_lifetime(identity_token),
            "refresh_valid_until": jwt_helper.token_lifetime(refresh_token),
            "user": user_data,
        }
    )
