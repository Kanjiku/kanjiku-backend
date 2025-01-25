import tomllib

from sanic import Sanic
from pathlib import Path
from functools import partial
from sanic.worker.loader import AppLoader

from kanjiku_api.Enums import SignMethod
from kanjiku_api import create_app, cli


if __name__ == "__main__":
    config_file = cli()
    cfg = tomllib.loads(Path(config_file).read_text())
    cfg["JWT"]["signmethod"] = SignMethod(cfg["JWT"].pop("algorithm"))
    loader = AppLoader(factory=partial(create_app, cfg))
    app = loader.load()

    app.prepare(
        host=cfg.get("listening_ip", "localhost"),
        port=cfg.get("port", 9999),
        dev=cfg.get("debug", False),
    )
    Sanic.serve(primary=app, app_loader=loader)
