import i18n

from uuid import uuid4
from sanic import Blueprint
from sanic.exceptions import BadRequest
from sanic.request import Request
from sanic.response import json as json_resp

from kanjiku_api.Utility.Decorators import get_id_token
from kanjiku_api.Exceptions import ParameterError
from kanjiku_api.data_models import Image, IdentityToken, User
from kanjiku_api.Utility import ImageHandler

image_bp = Blueprint("Image", "/Image")

from . import _uid


@image_bp.route("/", ["GET"], name="show_images")
@get_id_token
async def show_images(request: Request):
    """This function returns a list of all Images.

    openapi:
    ---
    parameters:
    - name: pagesize
      in: query
      description: Numbers of users per page
      required: false
      default: 25
    - name: page
      in: query
      description: which page of all users to display
      required: false
      default: 1
    responses:
      '200':
        content:
          application/json:
            type: object
            schema:
              properties:
                id:
                  type: integer
                  format: int64
                  example: 10
                name:
                  type: string
                  example: doggie
    """
    request_args: dict = request.args
    try:
        page = int(request_args.get("page", 1))
    except ValueError:
        raise ParameterError(
            {
                "msg": i18n.t("errors.parameter_error").format(parameter="page"),
                "msg_key": "errors.parameter_error",
            },
            400,
        )
    try:
        pagesize = int(request_args.get("pagesize", 25))
    except ValueError:
        raise ParameterError(
            {
                "msg": i18n.t("errors.parameter_error").format(parameter="pagesize"),
                "msg_key": "errors.parameter_error",
            },
            400,
        )
    image_count = await Image.all().count()
    images = (
        await Image.all()
        .order_by("-created_at")
        .offset((page - 1) * pagesize)
        .limit(pagesize)
        .values_list("filename", "uuid", "uploaded_by_id")
    )
    print(images)
    results = [
        {"uuid": str(uuid), "filename": filename, "uploader": str(uploaded_by)}
        for filename, uuid, uploaded_by in images
    ]

    return json_resp({"image_count": image_count, "images": results})


@image_bp.route("/", ["POST"], name="upload_image")
@get_id_token
async def upload_image(request: Request):
    id_token: IdentityToken = request.ctx.id_token
    if request.files is not None and len(request.files) != 1:
        raise BadRequest(
            {"msg": i18n.t("errors.to_many_files"), "msg_key": "errors.to_many_files"}
        )
    image_handler: ImageHandler = request.app.ctx.image_handler

    filename, raw_file = list(request.files.items())[0]
    file = raw_file[0].body
    try:
        filename = raw_file[0].name
    except Exception as exc:
        pass

    img_uuid = uuid4()
    await image_handler.create_file(file, str(img_uuid))

    # check if user has an old avatar
    user: User = await id_token.user
    img = await Image.create(uuid=img_uuid, filename=filename, uploaded_by=user)

    await request.app.dispatch(
        "user.image.uploaded",
        context={"img_uuid": img_uuid, "img_handler": image_handler},
    )

    return json_resp(
        {
            "msg": i18n.t("messages.image_uploaded"),
            "msg_key": "messages.image_uploaded",
        }
    )
