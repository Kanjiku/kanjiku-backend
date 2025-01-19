import i18n
import bcrypt

from datetime import date
from tortoise.exceptions import ValidationError
from sanic import Request
from sanic.response import json as json_resp

from kanjiku_api.data_models import User
from kanjiku_api.Exceptions import RegistrationFail
from . import user_bp


@user_bp.route("/register", ["POST"])
async def register(request: Request):

    request_body = request.json

    username = request_body.get("username", None)
    password = request_body.get("password", None)
    email = request_body.get("email", None)
    birthday = request_body.get("birthday", None)

    if birthday is not None:
        birthday = date.fromisoformat(birthday)

    if username is None or password is None or email is None:
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.missing_parameters"),
                "msg_key": "errors.missing_parameters",
            }
        )

    if await User.get_or_none(username=username) is not None:
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.username_taken").format(username=username),
                "msg_key": "errors.username_taken",
            }
        )

    if await User.get_or_none(email=email) is not None:
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.email_taken").format(email=email),
                "msg_key": "errors.email_taken",
            }
        )

    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    try:
        user = await User.create(
            username=username, password_hash=pw_hash, email=email, birthday=birthday
        )
    except ValidationError:
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.validation_error"),
                "msg_key": "errors.validation_error",
            }
        )

    return json_resp(
        {
            "msg": i18n.t("messages.user_created").format(
                username=request_body["username"]
            ),
            "msg_key": "messages.user_created",
        }
    )
