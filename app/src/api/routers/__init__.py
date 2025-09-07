from fastapi import APIRouter

from .item_router import item_router

group_router = APIRouter(prefix="/api/v1")

group_router.include_router(item_router)
