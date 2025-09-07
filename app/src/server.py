from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.api.routers import group_router
from src.db import init_db_tortoise


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Инициализация БД перед
    """
    await init_db_tortoise(_app)
    yield


def remove_response_from_openapi(app: FastAPI, code: str = "422"):
    """
    Удаляет указанный код ответа из OpenAPI схемы приложения FastAPI.
    """
    original_openapi = app.openapi

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = original_openapi()
        for path in openapi_schema["paths"].values():
            for method in path.values():
                responses = method.get("responses", {})
                if code in responses:
                    del responses[code]
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi


def create_app() -> FastAPI:
    """
    Сборка полного приложения
    """
    _app = FastAPI(
        title="DevOps API",
        docs_url="/docs",
        lifespan=lifespan,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(group_router)

    @_app.exception_handler(RequestValidationError)
    async def validation_exception(request: Request, e: RequestValidationError):
        payload = {
            "message": "Некорректные входные данные",
            "detail": e.errors()[0]["msg"],
            "body": getattr(e, "body", None),
        }

        return JSONResponse(status_code=400, content=payload)

    remove_response_from_openapi(_app, "422")

    return _app


app = create_app()
