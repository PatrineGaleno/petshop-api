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
    customer_name: str
    product_id: int
    product_name: str
    bought_quantity: int
    payment_form: str
    price_on_sale: Decimal
    date: datetime.date
    
    @staticmethod
    def resolve_product_name(obj):
        return obj.product.name

    @staticmethod
    def resolve_customer_name(obj):
        return obj.customer.get_full_name()


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
