import bcrypt
import tomllib
import logging

from sanic import Sanic
from pathlib import Path
from typing import Optional
from functools import partial
from sanic.worker.loader import AppLoader

from kanjiku_api.Enums import SignMethod
from kanjiku_api import create_app, cli
from kanjiku_api.data_models import User, Group

logger = logging.getLogger("kanjiku_backend")


async def prepare_db(
    _app,
    _loop,
    user_config: Optional[list[dict]] = None,
    group_config: Optional[list[dict]] = None,
):
    if group_config is not None:
        for group_data in group_config:
            group = await Group.get_or_none(name=group_data["name"])
            if group is not None:
                logger.info(
                    f"Group {group_data['name']} already exists skipping creation"
                )
                continue

            logger.info(f"creating group {group_data['name']}")

            group = await Group.create(**group_data)
            await group.save()

    if user_config is not None:
        for user_data in user_config:

            username = user_data["username"]
            password = user_data["password"]
            email = user_data.get("email", "donotreply@example.com")

            user = await User.get_or_none(username=username)
            if user is None:
                salt = bcrypt.gensalt()
                pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
                logger.info(f"creating user {username}")
                print(username, password, pw_hash)
                user = await User.create(
                    username=username, password_hash=pw_hash, email=email
                )

            user = await User.get(username=username)
            # add missing groups
            for group in user_data.get("groups", []):
                db_group = await Group.get(name=group)
                print("############", db_group)
                await user.groups.add(db_group)

            users_groups: list[Group] = await user.groups.all()
            for group in users_groups:
                if group.name in user_data.get("groups", []):
                    continue
                await user.groups.remove(group)

            await user.save()
            print(await user.serialize(True))


if __name__ == "__main__":
    config_file = cli()
    cfg = tomllib.loads(Path(config_file).read_text())
    cfg["JWT"]["signmethod"] = SignMethod(cfg["JWT"].pop("algorithm"))
    loader = AppLoader(factory=partial(create_app, cfg))
    app = loader.load()

    app.register_listener(
        partial(
            prepare_db,
            user_config=cfg.get("users", None),
            group_config=cfg.get("groups", None),
        ),
        "main_process_start",
    )

    app.prepare(
        host=cfg.get("listening_ip", "localhost"),
        port=cfg.get("port", 9999),
        dev=cfg.get("debug", False),
    )
    Sanic.serve(primary=app, app_loader=loader)
