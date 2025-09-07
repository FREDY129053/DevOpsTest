from tortoise import fields
from tortoise.models import Model
from tortoise.exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP

def validate_price(value):
    if not isinstance(value, Decimal):
        value = Decimal(str(value))

    if value < 0:
        raise ValidationError(f"Value '{value}' is not a positive number")
    
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class Item(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=128)
    price = fields.DecimalField(max_digits=12, decimal_places=2, validators=[validate_price])
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "items"