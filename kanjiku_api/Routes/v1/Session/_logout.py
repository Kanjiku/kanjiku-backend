import i18n

from sanic import Request, BadRequest
from uuid import UUID

from kanjiku_api.Exceptions import SessionError
from kanjiku_api.Utility import JWTHelper
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
    token_data, token_id = jwt_helper.token_data(id_token)
    request_data = None
    try:
        request_data = request.json
    except BadRequest:
        # if the request has no valid json ignore it
        pass
    if request_data is None:
        #if no json was provided we use an empty dict
        request_data = {}

    # check if the session is active
    IdentityToken.get(id=)

    if request_data.get("logout_all", False):
        # the user wants to destroy all Session

    raise ValueError(request_data)
