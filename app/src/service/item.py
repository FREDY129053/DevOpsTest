import src.repository.item as ItemRepo
from src.schemas.item import AddItem, ItemInfo, Stats
from src.schemas.msg import Message


async def get_stats() -> Message:
    count, avg_price = await ItemRepo.get_stats()

    return Message(msg=Stats(count=count, avg_price=avg_price).model_dump(), status_code=200)


async def list_items(offset: int, limit: int) -> Message:
    items = await ItemRepo.list_items(offset=offset, limit=limit)
    if items is None:
        return Message(
            is_error=True,
            status_code=500,
            msg="Ошибка получения списка товаров"
        )
    
    return Message(
        status_code=200,
        msg=[
            ItemInfo(
                id=item.id,
                name=item.name,
                price=float(item.price),
                created_at=str(item.created_at),
            ).model_dump()
            for item in items
        ],
    )


async def add_item(item_data: AddItem) -> Message:
    item = await ItemRepo.add_item(name=item_data.name, price=item_data.price)
    if item is None:
        return Message(is_error=True, msg="server error", status_code=500)

    item_out = ItemInfo(
        id=item.id,
        name=item.name,
        price=float(item.price),
        created_at=str(item.created_at),
    )

    return Message(status_code=201, msg=item_out.model_dump())
