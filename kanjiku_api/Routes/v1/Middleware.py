from sanic import Request
from jwt.exceptions import InvalidTokenError
from kanjiku_api.Utility import JWTHelper


async def add_token_info(request: Request):
    id_token = request.cookies.get("IdentityToken", None)
    refresh_token = request.cookies.get("RefreshToken", None)

    user_info = None

    if id_token is not None:
        helper: JWTHelper = request.app.ctx.jwt
        try:
            user_info, _ = helper.token_data(id_token)
        except InvalidTokenError:
            pass

    request.ctx.id_token = id_token
    request.ctx.refresh_token = refresh_token
    request.ctx.user_info = user_info
