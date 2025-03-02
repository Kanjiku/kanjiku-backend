from sanic import Blueprint

image_bp = Blueprint("Image", "/Image")

from . import _uid