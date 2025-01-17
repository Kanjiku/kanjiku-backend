import i18n

from sanic import Request
from sanic.response import json as json_resp

from . import user_bp


@user_bp.route("/",["GET"])
def show_user(request:Request):
    return json_resp({"greeting": i18n.t("errors.hello_world")})
