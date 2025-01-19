from sanic import Blueprint

user_bp = Blueprint("User", "/User")

from . import _show, _register
