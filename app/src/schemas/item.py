from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field, ValidationError


def _is_valid_color(value) -> Decimal:
    if not isinstance(value, Decimal):
        raise ValidationError(f"{value} is not valid number")

    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class AddItem(BaseModel):
    name: str = Field(description="Наименование товара", min_length=1, max_length=128)
    price: Annotated[Decimal, AfterValidator(_is_valid_color)] = Field(
        description="Цена товара", gt=0, le=10_000_000, examples=["100", "100.0"]
    )


class ItemInfo(BaseModel):
    id: int = Field(description="ID товара")
    name: str = Field(description="Наименование товара")
    price: float = Field(description="Цена товара")
    created_at: str = Field(description="Дата создания товара")

    class Config:
        from_attributes = True


class Stats(BaseModel):
    count: int = Field(description="Кол-во записей в БД")
    avg_price: float = Field(description="Средняя цена всех товаров")
