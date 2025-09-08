import os

def _build_db_uri() -> str:
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASS", "postgres")
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", 5432))
    name = os.getenv("DB_NAME", "test")

    return f"postgres://{user}:{password}@{host}:{port}/{name}"

TORTOISE_ORM = {
    "connections": {
        "default": _build_db_uri()
    },
    "apps": {
        "models": {
            "models": ["src.db.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
