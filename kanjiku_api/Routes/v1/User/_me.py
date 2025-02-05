import i18n
import bcrypt
import datetime

from sanic import Request
from sanic.exceptions import BadRequest
from sanic.response import json as json_resp

from kanjiku_api.Utility import JWTHelper
from kanjiku_api.Exceptions import SessionError
from kanjiku_api.data_models import User, IdentityToken
from kanjiku_api.Decorators import request_contains_valid_json
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


@user_bp.route("/me", ["PATCH"])
@request_contains_valid_json
async def update_user_by_id(request: Request):

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
    request_data = request.json

    birthday = request_data.get("birthday", None)
    email = request_data.get("email", None)
    new_password = request_data.get("password", None)
    old_password = request_data.get("old_password", None)

    # return a success message
    resp = json_resp(
        {
            "msg": i18n.t("messages.update_successfull"),
            "msg_key": "messages.update_successfull",
        }
    )

    if (
        birthday is None
        and email is None
        and new_password is None
        and old_password is None
    ):
        raise BadRequest(
            {
                "msg": i18n.t("errors.no_data_to_update"),
                "msg_key": "errors.no_data_to_update",
            }
        )

    if birthday is not None:
        user.birthday = datetime.date.fromisoformat(birthday)

    if email is not None:
        user.email = email

    if new_password is not None and old_password is not None:
        if not bcrypt.checkpw(old_password.encode("utf-8"), user.password_hash):
            raise BadRequest(
                {
                    "msg": i18n.t("errors.update_wrong_password"),
                    "msg_key": "errors.update_wrong_password",
                },
            )
        
        salt = bcrypt.gensalt()
        pw_hash = bcrypt.hashpw(new_password.encode("utf-8"), salt)
        user.password_hash = pw_hash

    await user.save()

    # get all identity tokens and delete them
    tokens_to_delete = await user.identity_tokens.all()

    # delete them
    for token in tokens_to_delete:
        await token.delete()

    # tell the browser to delete the tokens as well
    resp.delete_cookie("IdentityToken")
    resp.delete_cookie("RefreshToken")

    return resp
