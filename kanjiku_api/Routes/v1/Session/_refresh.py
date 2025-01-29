import i18n

from sanic import Request
from sanic.response import json as json_resp

from kanjiku_api.Utility import JWTHelper
from kanjiku_api.Exceptions import SessionError
from . import session_bp


@session_bp.route("/refresh", ["GET"])
async def refresh(request: Request):
    refresh_token = request.cookies.get("RefreshToken", None)
    if refresh_token is None:
        raise SessionError(
            {
                "msg": i18n.t("errors.no_refresh_token_provided"),
                "msg_key": "errors.no_refresh_token_provided",
            },
            status_code=400,
        )

    jwt_helper: JWTHelper = request.app.ctx.jwt

    id_token, refresh_token = await jwt_helper.renew_tokens(refresh_token)

    resp = json_resp(
        {
            "msg": i18n.t("messages.session_refreshed"),
            "msg_key": "messages.session_refreshed",
        }
    )
    resp.cookies.add_cookie(
        "IdentityToken",
        id_token,
        httponly=True,
        max_age=jwt_helper.valid_minutes_id * 60,
    )
    resp.cookies.add_cookie(
        "RefreshToken",
        refresh_token,
        httponly=True,
        max_age=jwt_helper.valid_minutes_refresh * 60,
    )

    return resp
