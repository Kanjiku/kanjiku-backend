import i18n
import bcrypt
import datetime

from uuid import uuid4
from sanic import Request
from typing import Optional
from sanic.exceptions import BadRequest
from sanic.response import json as json_resp

from kanjiku_api.Utility import JWTHelper, ImageHandler
from kanjiku_api.Exceptions import SessionError
from kanjiku_api.data_models import User, IdentityToken, Image
from kanjiku_api.Decorators import request_contains_valid_json, get_id_token
from . import user_bp


@user_bp.route("/me", ["GET"], name="me")
@get_id_token
async def me(request: Request):

    id_token: IdentityToken = request.ctx.id_token

    user: User = await id_token.user

    resp_data = await user.serialize(True)

    return json_resp(resp_data)


@user_bp.route("/me", ["PATCH"], name="update_me")
@request_contains_valid_json
@get_id_token
async def update_me(request: Request):
    id_token: IdentityToken = request.ctx.id_token
    user: User = await id_token.user
    request_data = request.json

    birthday = request_data.get("birthday", None)
    email = request_data.get("email", None)
    new_password = request_data.get("password", None)
    old_password = request_data.get("old_password", None)

    # return a success message
    resp = json_resp(
        {
            "msg": i18n.t("messages.update_successfull"),
            "msg_key": "messages.update_successfull",
        }
    )

    if (
        birthday is None
        and email is None
        and new_password is None
        and old_password is None
    ):
        raise BadRequest(
            {
                "msg": i18n.t("errors.no_data_to_update"),
                "msg_key": "errors.no_data_to_update",
            }
        )

    if birthday is not None:
        user.birthday = datetime.date.fromisoformat(birthday)

    if email is not None:
        user.email = email

    if new_password is not None and old_password is not None:
        if not bcrypt.checkpw(old_password.encode("utf-8"), user.password_hash):
            raise BadRequest(
                {
                    "msg": i18n.t("errors.update_wrong_password"),
                    "msg_key": "errors.update_wrong_password",
                },
            )

        salt = bcrypt.gensalt()
        pw_hash = bcrypt.hashpw(new_password.encode("utf-8"), salt)
        user.password_hash = pw_hash

    await user.save()

    # get all identity tokens and delete them
    tokens_to_delete = await user.identity_tokens.all()

    # delete them
    for token in tokens_to_delete:
        await token.delete()

    # tell the browser to delete the tokens as well
    resp.delete_cookie("IdentityToken")
    resp.delete_cookie("RefreshToken")

    return resp


@user_bp.route("/me", ["DELETE"], name="delete_me")
@get_id_token
async def delete_me(
    request: Request,
):
    id_token: IdentityToken = request.ctx.id_token
    user: User = await id_token.user

    user_avatar: Optional[Image] = await user.avatar
    if user_avatar is not None:
        image_handler: ImageHandler = request.app.ctx.image_handler
        await image_handler.remove_file(str(user_avatar.uuid))
        await user_avatar.delete()

    await user.delete()
    resp = json_resp(
        {"msg": i18n.t("messages.user_deleted"), "msg_key": "messages.user_deleted"}
    )
    # tell the browser to delete the tokens as well
    resp.delete_cookie("IdentityToken")
    resp.delete_cookie("RefreshToken")
    return resp


@user_bp.route("/me/avatar", ["POST"], name="upload_avatar")
@get_id_token
async def upload_avatar(request: Request):
    id_token: IdentityToken = request.ctx.id_token
    if request.files is not None and len(request.files) != 1:
        raise BadRequest(
            {"msg": i18n.t("errors.to_many_files"), "msg_key": "errors.to_many_files"}
        )
    image_handler: ImageHandler = request.app.ctx.image_handler
    filename, file = list(request.files.items())[0]
    file = file[0].body

    img_uuid = uuid4()
    await image_handler.create_file(file, str(img_uuid))

    # check if user has an old avatar
    user: User = await id_token.user

    user_avatar: Optional[Image] = await user.avatar
    removed_old_avatar = False
    if user_avatar is not None:
        await image_handler.remove_file(str(user_avatar.uuid))
        removed_old_avatar = True
        await user_avatar.delete()

    img = await Image.create(uuid=img_uuid, filename=filename)
    user.avatar = img
    await user.save()

    await request.app.dispatch(
        "user.avatar.uploaded",
        context={"img_uid": img_uuid, "img_handler": image_handler},
    )

    return json_resp(
        {
            "msg": i18n.t("messages.avatar_uploaded"),
            "msg_key": "messages.avatar_uploaded",
            "removed_old_avatar": removed_old_avatar,
        }
    )
