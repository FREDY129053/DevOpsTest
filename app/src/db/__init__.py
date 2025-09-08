from fastapi import FastAPI
from tortoise import Tortoise


async def init_db_tortoise(app: FastAPI) -> None:
    """
    Инициализация Tortoise.
    - берём URL из app.state.db_url
    - по дефолту считываем данные из .env
    """
    db_url = getattr(app.state, "db_url", None)
    if db_url:
        tortoise_config = {
            "connections": {"default": db_url},
            "apps": {
                "models": {
                    "models": ["src.db.models", "aerich.models"],
                    "default_connection": "default",
                }
            },
        }

        await Tortoise.init(config=tortoise_config)
        await Tortoise.generate_schemas()
    else:
        from .config import TORTOISE_ORM

        await Tortoise.init(config=TORTOISE_ORM)
