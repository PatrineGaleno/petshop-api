from ninja import Schema, FilterSchema
from typing import Optional


class UserFilter(FilterSchema):
    id: Optional[int] = None


class UserIn(Schema):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str
    address: str


class UserOut(Schema):
    id: int
    username: str
    email: str
    role: str
    first_name: str
    last_name: str
    phone: str
    address: str
