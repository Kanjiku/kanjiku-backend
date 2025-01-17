from sanic import Sanic
from sanic.worker.loader import AppLoader
from functools import partial

from kanjiku_api import create_app


if __name__ == "__main__":
    loader = AppLoader(factory=partial(create_app, "kanjiku_api"))
    app = loader.load()
    app.prepare(port=9999, dev=True)
    Sanic.serve(primary=app, app_loader=loader)
