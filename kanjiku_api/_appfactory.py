import i18n

from sanic import Sanic, text, Request
from sanic_ext import Extend
from sanic.response import json

from tortoise import Tortoise, connections
from tortoise.log import logger

from kanjiku_api.Routes.v1 import v1_bp
from kanjiku_api.Routes import generic_bp
from kanjiku_api.Exceptions import RegistrationFail

i18n.load_path.append("./locales")
i18n.set("locale", "de")
i18n.set("file_format", "yaml")
i18n.set("filename_format", "{namespace}.{format}")
i18n.set("skip_locale_root_data", True)
i18n.set("use_locale_dirs", True)
i18n.load_everything()


def attach_endpoints(app: Sanic):
    @app.get("/")
    async def hello_world(request):
        return text("Hello, world.")

    app.blueprint(v1_bp)
    app.blueprint(generic_bp)

    @app.listener("after_server_stop")
    async def close_orm(app, loop):  # pylint: disable=W0612
        await connections.close_all()
        logger.info("Tortoise-ORM shutdown")

    async def tortoise_init() -> None:
        await Tortoise.init(
            db_url="sqlite://:memory:",
            modules={"data_models": ["kanjiku_api.data_models"]},
        )
        logger.info(
            "Tortoise-ORM started, %s, %s", connections._get_storage(), Tortoise.apps
        )  # pylint: disable=W0212
        await Tortoise.generate_schemas()

    @app.listener("before_server_start")
    async def init_orm(app, loop):  # pylint: disable=W0612
        await tortoise_init()

    @app.listener("main_process_start")
    async def init_orm_main(app, loop):  # pylint: disable=W0612
        await tortoise_init()
        logger.info("Tortoise-ORM generating schema")
        await Tortoise.generate_schemas()

    @app.exception(RegistrationFail)
    async def handle_registration_fail(request:Request, exc:RegistrationFail):
        return json(exc.message, status=exc.status_code)


def create_app(app_name: str) -> Sanic:

    app = Sanic(app_name)
    attach_endpoints(app)
    app.config.CORS_ORIGINS = "*"
    Extend(app)

    return app
