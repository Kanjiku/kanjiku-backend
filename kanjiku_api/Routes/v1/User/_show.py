import i18n

from sanic import Request
from sanic.response import json as json_resp

from kanjiku_api.data_models import User
from kanjiku_api.Exceptions import UserDoesNotExist, ParameterError
from . import user_bp


@user_bp.route("/", ["GET"])
async def show_user(request: Request):
    """This function returns a list of all Users.

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
    user_count = await User.all().count()
    users = (
        await User.all()
        .offset((page - 1) * pagesize)
        .limit(pagesize)
        .values_list("username", "id")
    )
    print(users)
    for user in users:
        username, uid = user
        print(username, str(uid))
    results = {str(uid):username for username, uid in users}

    return json_resp({"user_count": user_count, "users":results})


@user_bp.route("/<user_id:int>", ["GET"])
async def show_user_by_id(request: Request, user_id: int):
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise UserDoesNotExist(
            {
                "msg": i18n.t("errors.user_does_not_exist").format(id=user_id),
                "msg_key": "errors.user_does_not_exist",
            },
            status_code=404,
        )

    avatar = await user.avatar
    if avatar is not None:
        avatar = avatar.uuid

    groups = await user.groups.all().values_list("name", flat=True)

    repsonse_data = {
        "id": user.id,
        "username": user.username,
        "avatar": avatar,
        "groups": groups,
        "member_since": user.created_at.strftime("%d/%m/%Y"),
    }

    if False:
        birthday = user.birthday
        if birthday is not None:
            birthday = birthday.isoformat()
        repsonse_data["birthday"] = birthday
        repsonse_data["email"] = user.email

    return json_resp(repsonse_data)
