import os

from fastapi import FastAPI
from tortoise import Tortoise


async def init_db_tortoise(app: FastAPI) -> None:
    """
    Инициализация Tortoise.
    - берём URL из app.state.db_url
    - по дефолту считываем данные из .env
    """
    if getattr(app.state, "db_url", None):
        db_url = getattr(app.state, "db_url")
    else:
        db_url = f"postgres://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"

    tortoise_config = {
        "connections": {"default": db_url},
        "apps": {
            "models": {
                "models": ["src.db.models"],
                "default_connection": "default",
            }
        },
    }

    await Tortoise.init(config=tortoise_config)
    await Tortoise.generate_schemas()
