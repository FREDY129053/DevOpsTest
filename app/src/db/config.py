import os


def _build_db_uri() -> str:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = int(os.getenv("POSTGRES_PORT", 5432))
    name = os.getenv("POSTGRES_DB", "test")

    return f"postgres://{user}:{password}@{host}:{port}/{name}"


TORTOISE_ORM = {
    "connections": {"default": _build_db_uri()},
    "apps": {
        "models": {
            "models": ["src.db.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
