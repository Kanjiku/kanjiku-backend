from sanic import Blueprint
from sanic.response import json as json_resp

from .User import user_bp

v1_bp = Blueprint.group(user_bp, url_prefix="/v1")
