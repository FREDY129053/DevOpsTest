import src.service.item as ItemService
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from src.schemas.item import AddItem, ItemInfo, Stats
from src.schemas.msg import Error, Error_400

item_router = APIRouter(prefix="/items", tags=["Items"])


@item_router.get(
    "/stats",
    response_model=Stats,
    responses={
        500: {
            "description": "Server error",
            "content": {"application/json": {"schema": Error.model_json_schema()}},
        }
    },
)
async def get_items_stats():
    """
    ## Получение статистики товаров
    """
    result = await ItemService.get_stats()
    if result.is_error:
        raise HTTPException(status_code=result.status_code, detail=result.msg)

    return JSONResponse(content=result.msg, status_code=result.status_code)


@item_router.get(
    "/items",
    response_model=list[ItemInfo],
    responses={
        500: {
            "description": "Server error",
            "content": {"application/json": {"schema": Error.model_json_schema()}},
        }
    },
)
async def list_items(
    page: int = Query(1, ge=1, description="Page number"),
    count: int = Query(10, ge=1, description="Items per page"),
):
    """
    ## Получение списка товаров с пагинацией
    """
    offset = (page - 1) * count
    result = await ItemService.list_items(offset=offset, limit=count)

    if result.is_error:
        raise HTTPException(status_code=result.status_code, detail=result.msg)

    return JSONResponse(content=result.msg, status_code=result.status_code)


@item_router.post(
    "/add",
    response_model=ItemInfo,
    responses={
        400: {
            "description": "Invalid user input",
            "content": {"application/json": {"schema": Error_400.model_json_schema()}},
        },
        500: {
            "description": "Server error",
            "content": {"application/json": {"schema": Error.model_json_schema()}},
        },
    },
)
async def add_item(item_data: AddItem):
    """
    ## Создание записи товара
    """
    result = await ItemService.add_item(item_data)
    if result.is_error:
        raise HTTPException(status_code=result.status_code, detail=result.msg)

    return JSONResponse(content=result.msg, status_code=result.status_code)
