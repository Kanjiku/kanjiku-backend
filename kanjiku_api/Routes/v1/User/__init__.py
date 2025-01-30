import i18n

from sanic import Blueprint, Request
from sanic.response import json as json_resp

user_bp = Blueprint("User", "/User")

from kanjiku_api.data_models import User
from kanjiku_api.Exceptions import ParameterError
from . import _show, _register, _me


@user_bp.route("/", ["GET"])
async def show_users(request: Request):
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
        .values_list("username", "uuid")
    )
    print(users)
    for user in users:
        username, uid = user
        print(username, str(uid))
    results = {str(uuid): username for username, uuid in users}

    return json_resp({"user_count": user_count, "users": results})
