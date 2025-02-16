import i18n

from sanic import Sanic, Request
from uuid import UUID

from kanjiku_api.data_models import Image
from kanjiku_api.Utility import ImageHandler
from kanjiku_api.Exceptions import ImageDoesNotExist

from . import image_bp


@image_bp.route("/<image_id:uuid>", ["GET"])
async def get_image(request: Request, image_id: UUID):
    image = await Image.get_or_none(uuid=image_id)
    if image is None:
        raise ImageDoesNotExist(
            {
                "msg": i18n.t("errors.image_does_not_exist"),
                "msg_key": "errors.image_does_not_exist",
            },
            status_code=404,
        )

    image_handler: ImageHandler = request.app.ctx.image_handler

    return await image_handler.get_file(image_id, image.filename)


from . import image_bp


@image_bp.route("/<image_id:uuid>/thumbnail", ["GET"])
async def get_image_thumbnail(request: Request, image_id: UUID):
    image = await Image.get_or_none(uuid=image_id)
    if image is None:
        raise ImageDoesNotExist()

    image_handler: ImageHandler = request.app.ctx.image_handler
    if image_handler.exists(f"{image_id}_thumbnail"):
        img_resp = await image_handler.get_file(
            f"{image_id}_thumbnail", f"{image.filename}_thumbnail.webp"
        )
    else:
        img_resp = await image_handler.get_file(image_id, image.filename)

    return img_resp
