import i18n

from sanic import Sanic, text
from sanic_ext import Extend
from tortoise.contrib.sanic import register_tortoise

from kanjiku_api.Routes.v1 import v1_bp
from kanjiku_api.Routes import generic_bp

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


def create_app(app_name: str) -> Sanic:

    app = Sanic(app_name)
    attach_endpoints(app)
    register_tortoise(
        app,
        db_url="sqlite://:memory:",
        modules={"data_models": ["kanjiku_api.data_models"]},
        generate_schemas=True,
    )
    app.config.CORS_ORIGINS = "*"
    Extend(app)
    return app
