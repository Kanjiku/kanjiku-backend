import i18n

from sanic_ext import Extend
from tortoise.log import logger
from sanic.response import json
from jwt import InvalidTokenError
from sanic import Sanic, text, Request
from tortoise import Tortoise, connections


from kanjiku_api.Routes.v1 import v1_bp
from kanjiku_api.Routes import generic_bp
from kanjiku_api.Exceptions import (
    RegistrationFail,
    UserDoesNotExist,
    LoginError,
    ParameterError,
    ImageDoesNotExist,
)
from kanjiku_api.Utility import JWTHelper, ImageHandler
from kanjiku_api.Utility.SignalHandler import create_thumbnail

i18n.load_path.append("./locales")
i18n.set("locale", "de")
i18n.set("file_format", "yaml")
i18n.set("filename_format", "{namespace}.{format}")
i18n.set("skip_locale_root_data", True)
i18n.set("use_locale_dirs", True)
i18n.load_everything()


def attach_tortoise(app: Sanic, db_url: str = "sqlite://:memory:"):

    async def tortoise_init() -> None:
        await Tortoise.init(
            db_url=db_url,
            modules={"data_models": ["kanjiku_api.data_models"]},
        )
        logger.info(
            "Tortoise-ORM started, %s, %s", connections._get_storage(), Tortoise.apps
        )  # pylint: disable=W0212
        await Tortoise.generate_schemas(safe=True)

    @app.listener("after_server_stop")
    async def close_orm(app, loop):  # pylint: disable=W0612
        await connections.close_all()
        logger.info("Tortoise-ORM shutdown")

    @app.listener("before_server_start")
    async def init_orm(app, loop):  # pylint: disable=W0612
        await tortoise_init()

    @app.listener("main_process_start")
    async def init_orm_main(app, loop):  # pylint: disable=W0612
        await tortoise_init()
        logger.info("Tortoise-ORM generating schema")
        await Tortoise.generate_schemas()


def attach_signal_handlers(app: Sanic):
    app.add_signal(create_thumbnail, "user.avatar.uploaded")


def attach_endpoints(app: Sanic, cors_origin: str):

    app.blueprint(v1_bp)
    app.blueprint(generic_bp)

    app.config.CORS_ORIGINS = cors_origin
    app.config.CORS_SUPPORTS_CREDENTIALS = True


def attach_error_handlers(app: Sanic):
    @app.exception(RegistrationFail, UserDoesNotExist, LoginError, ParameterError)
    async def handle_registration_fail(request: Request, exc: RegistrationFail):
        return json(exc.message, status=exc.status_code)

    @app.exception(ImageDoesNotExist)
    async def handle_image_not_found(request: Request, exc: ImageDoesNotExist):
        return json(
            {
                "msg": i18n.t("errors.image_does_not_exist"),
                "msg_key": "errors.image_does_not_exist",
            },
            status=404,
        )

    @app.exception(InvalidTokenError)
    async def handle_decode_error(request: Request, exc: InvalidTokenError):
        return json(
            {
                "msg": i18n.t("errors.jwt_error"),
                "msg_key": "errors.jwt_error",
            },
            400,
        )


def create_app(config: dict) -> Sanic:
    app_name = config.get("app_name", "ImageUploadBackend")
    db_url = config.get("db_url", "sqlite://:memory:")
    app = Sanic(app_name)
    attach_endpoints(app, config["cors_origin"])
    attach_tortoise(app, db_url)
    attach_signal_handlers(app)
    attach_error_handlers(app)
    app.config.OAS_UI_REDOC = False
    app.config.OAS_UI_DEFAULT = "swagger"
    app.ctx.CFG = config

    app.ctx.image_handler = ImageHandler(**config["Files"])
    app.ctx.jwt = JWTHelper(**config["JWT"])

    Extend(app)

    return app
