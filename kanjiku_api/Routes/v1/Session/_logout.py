from sanic import Request

from . import session_bp


@session_bp.route("/logout", ["POST"])
async def logout(request: Request):
    raise NotImplementedError()