from decimal import Decimal

from src.db.models import Item
from tortoise.functions import Avg, Count


async def add_item(name: str, price: Decimal) -> Item | None:
    try:
        return await Item.create(name=name, price=price)
    except Exception:
        return None


async def get_stats() -> tuple[int, float]:
    items = await Item.annotate(avg_price=Avg("price"), count=Count("id")).values(
        "avg_price", "count"
    )
    res = items[0]

    return res["count"], 0 if res["avg_price"] is None else float(res["avg_price"])

async def list_items(offset: int, limit: int) -> list[Item] | None:
    try:
        return await Item.all().offset(offset).limit(limit)
    except Exception:
        return None