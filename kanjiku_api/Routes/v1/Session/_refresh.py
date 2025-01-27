from sanic import Request
from sanic.response import json as json_resp

from kanjiku_api.Utility import JWTHelper
from . import session_bp


@session_bp.route("/refresh", ["POST"])
async def refresh(request: Request):
    request_data = request.json
    refresh_token = request_data.get("refresh_token", None)
    jwt_helper: JWTHelper = request.app.ctx.jwt

    id_token, refresh_token = await jwt_helper.renew_tokens(refresh_token)

    return json_resp({"id_token": id_token, "refresh_token": refresh_token})
