from sanic import Blueprint

generic_bp = Blueprint("generic", "/")

from kanjiku_api.Routes import _version