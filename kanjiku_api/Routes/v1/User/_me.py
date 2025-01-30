import i18n
import bcrypt

from datetime import date
from tortoise.exceptions import ValidationError
from sanic import Request
from sanic.response import json as json_resp

from kanjiku_api.data_models import User, IdentityToken
from kanjiku_api.Exceptions import SessionError
from kanjiku_api.Utility import JWTHelper
from . import user_bp


@user_bp.route("/me", ["GET"])
async def me(request: Request):

    if request.ctx.id_token is None:
        raise SessionError(
            {
                "msg": i18n.t("errors.no_session"),
                "msg_key": "errors.no_session",
            },
            status_code=400,
        )

    jwt_helper: JWTHelper = request.app.ctx.jwt

    _, id_token_id = jwt_helper.token_data(request.ctx.id_token)

    id_token = await IdentityToken.get_or_none(uuid=id_token_id)

    if id_token is None:
        raise SessionError(
            {
                "msg": i18n.t("errors.no_session"),
                "msg_key": "errors.no_session",
            },
            status_code=400,
        )

    user: User = await id_token.user

    resp_data = await user.serialize(True)

    return json_resp(resp_data)
