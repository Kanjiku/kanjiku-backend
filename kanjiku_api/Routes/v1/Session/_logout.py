import i18n

from uuid import UUID
from datetime import datetime
from jwt import InvalidTokenError
from sanic import Request, BadRequest
from sanic.response import json as json_resp

from kanjiku_api.Utility import JWTHelper
from kanjiku_api.Exceptions import SessionError
from kanjiku_api.data_models import IdentityToken, User
from . import session_bp


@session_bp.route("/logout", ["POST"])
async def logout(request: Request):
    id_token = request.cookies.get("IdentityToken", None)
    print(id_token)
    if id_token is None:
        raise SessionError(
            {
                "msg": i18n.t("errors.no_session"),
                "msg_key": "errors.no_session",
            },
            status_code=400,
        )

    jwt_helper: JWTHelper = request.app.ctx.jwt
    _, token_id = jwt_helper.token_data(id_token)
    request_data = None
    try:
        request_data = request.json
    except BadRequest:
        # if the request has no valid json ignore it
        pass
    if request_data is None:
        # if no json was provided we use an empty dict
        request_data = {}

    # convert token id
    try:
        token_id = UUID(token_id)
    except ValueError:
        # if the UUID is invalid
        raise InvalidTokenError()

    # check if session is active
    id_token_obj = await IdentityToken.get_or_none(id=token_id)
    if id_token_obj is None:
        raise SessionError(
            {
                "msg": i18n.t("errors.no_session"),
                "msg_key": "errors.no_session",
            },
            status_code=400,
        )

    if id_token_obj.valid_until > datetime.now():
        raise SessionError(
            {
                "msg": i18n.t("errors.session_expired"),
                "msg_key": "errors.session_expired",
            },
            status_code=400,
        )

    tokens_to_delete: list[IdentityToken] = []

    if request_data.get("logout_all", False):
        # the user wants to destroy all Sessions
        # so we need to get all IdentityTokens belonging to the user
        user: User = await id_token_obj.user
        # add them to the list of tokens to delete
        tokens_to_delete = await user.identity_tokens.all()
    else:
        # if the user wants to log out jsut this session
        # only add the current token to the list of tokens to be deleted
        tokens_to_delete.append(id_token_obj)

    # finaly delete the tokens
    for token in tokens_to_delete:
        await token.delete()

    # return a success message
    resp = json_resp(
        {
            "msg": i18n.t("messages.logout_success"),
            "msg_key": "messages.logout_success",
        }
    )

    # tell the browser to delete the tokens as well
    resp.delete_cookie("IdentityToken")
    resp.delete_cookie("RefreshToken")

    return resp
