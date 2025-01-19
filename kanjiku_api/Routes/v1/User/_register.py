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
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

    if username is None or password is None or email is None:
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.missing_parameters"),
                "msg_key": "errors.missing_parameters",
            }
        )
    # see if the user provided a birthday and if so convert it to a date object
    try:
        if birthday is not None:
            birthday = date.fromisoformat(birthday)
    except ValueError:
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.birthday_invalid"),
                "msg_key": "errors.birthday_invalid",
            }
        )
    # see if the user provided email is not taken
    try:
        if await User.get_or_none(username=username) is not None:
            raise RegistrationFail(
                {
                    "msg": i18n.t("errors.username_taken").format(username=username),
                    "msg_key": "errors.username_taken",
                }
            )
    except ValidationError:
        # this will get thrown if the email does not match the email regex
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.username_invalid"),
                "msg_key": "errors.username_invalid",
            }
        )
    # see if the username is already taken
    try:
        if await User.get_or_none(email=email) is not None:
            raise RegistrationFail(
                {
                    "msg": i18n.t("errors.email_taken").format(email=email),
                    "msg_key": "errors.email_taken",
                }
            )
    except ValidationError:
        # this will get thrown if the username is to short
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.email_invalid"),
                "msg_key": "errors.email_invalid",
            }
        )
    try:
        user = await User.create(
            username=username, password_hash=pw_hash, email=email, birthday=birthday
        )
        await user.save()
    except ValidationError:
        # this error should not be possible because we already checked the email and username for validity
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
