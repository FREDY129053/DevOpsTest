import os

from dotenv import load_dotenv


def load_environment():
    """Загрузка перемнных среды из файла"""
    if os.getenv("ENV_TYPE", "prod") == "prod":
        return

    env_file = "../.env"

    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
        print("\033[32mINFO\033[0m:\t  env vars loaded")
    else:
        print(f"\033[31mERROR\033[0m:\t  {env_file} not found in main dir! Create it!!!")


def validate_environment():
    """Проверка переменных среды"""
    required_vars = [
        "SERVER_PORT",
        "SERVER_HOST",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required env vars: {missing}")
