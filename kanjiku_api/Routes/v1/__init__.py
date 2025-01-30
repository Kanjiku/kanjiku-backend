from sanic import Blueprint
from sanic.response import json as json_resp

from .User import user_bp
from .Session import session_bp
from .Middleware import add_token_info

v1_bp = Blueprint.group(user_bp, session_bp, url_prefix="/v1")
v1_bp.middleware(add_token_info, "request")
