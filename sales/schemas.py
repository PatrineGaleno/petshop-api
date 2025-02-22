from ninja import Schema, FilterSchema
from typing import Optional
from decimal import Decimal
import datetime


class SaleFilter(FilterSchema):
    id: Optional[int] = None
    customer_id: Optional[int] = None
    product_id: Optional[int] = None


class SaleIn(Schema):
    product_id: int
    bought_quantity: int
    payment_form: str


class SaleOut(Schema):
    id: int
    customer_id: int
    product_id: int
    bought_quantity: int
    payment_form: str
    price_on_sale: Decimal
    status: str
    date: datetime.date


class ProductFilter(FilterSchema):
    id: Optional[int] = None
    

class ProductIn(Schema):
    name: str
    description: str
    price: Decimal
    category_id: int


class ProductOut(Schema):
    id: int
    name: str
    price: Decimal
    current_quantity: int
    category_id: int
