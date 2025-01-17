from sanic import Blueprint, Request

user_bp = Blueprint("User", "/User")

from . import _show
