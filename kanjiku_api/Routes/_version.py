from sanic import Request
from sanic.response import json as json_resp

from kanjiku_api import __version__
from kanjiku_api.Routes import generic_bp


@generic_bp.route("/version", ["GET"])
def show_version(request: Request):
    return json_resp({"version": __version__})
