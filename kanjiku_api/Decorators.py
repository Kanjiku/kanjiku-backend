import jwt
import i18n

from uuid import UUID
from sanic import Request
from functools import wraps
from jwt import InvalidTokenError
from sanic.exceptions import BadRequest

from kanjiku_api.Utility import JWTHelper
from kanjiku_api.Exceptions import PermissionError, SessionError
from kanjiku_api.data_models import IdentityToken

auth_error = PermissionError(
    {
        "msg": i18n.t("errors.permission_error"),
        "msg_key": "errors.permission_error",
    },
    401,
)


def permission_required(*permissions: str, check_db: bool = False):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):

            # get ID token if provided
            id_token = request.cookies.get("IdentityToken", None)

            if id_token is None:
                # raise auth error if no id token was provided
                raise auth_error

            # get token data
            helper: JWTHelper = request.app.ctx.jwt
            try:
                user_info, _ = helper.token_data(id_token)
            except InvalidTokenError:
                pass

            # check if the user has the required permissions
            for perm in permissions:
                if not user_info.get("permissions", {}).get(perm, False):
                    raise auth_error

            # do the db lookup if requested
            if check_db:
                id_token_id = jwt.get_unverified_header(id_token).get("kid", None)

                if id_token_id is None:
                    raise auth_error
                try:
                    id_token_id = UUID(id_token_id)
                except ValueError:
                    raise auth_error

                id_token_obj = IdentityToken.get_or_none(id=id_token_id)

                if id_token_obj is None:
                    raise auth_error
                # we don't check the token lifetime here
                # because it should already be done by
                # the helper.token_data call

            response = await f(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator(decorator)


def request_contains_valid_json():
    def decorator(f):
        @wraps(f)
        async def decorated_req(request: Request, *args, **kwargs):
            try:
                request_content = request.json
                if not isinstance(request_content, dict):
                    raise BadRequest
            except BadRequest:
                raise BadRequest(
                    {
                        "msg": i18n.t("errors.request_invalid"),
                        "msg_key": "errors.errors.request_invalid",
                    }
                )

            response = await f(request, *args, **kwargs)
            return response

        return decorated_req

    return decorator


def get_id_token():
    def decorator(f):
        wraps(f)
        async def id_token_decorator(request: Request, *args, **kwargs):
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

            response = await f(request, id_token = id_token, *args, **kwargs)
            return response
        return id_token_decorator
    return decorator