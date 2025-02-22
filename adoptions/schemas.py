from ninja import Schema, FilterSchema
from typing import Optional
from decimal import Decimal
import datetime


class AdoptionFilter(FilterSchema):
    id: Optional[int] = None
    customer_id: Optional[int] = None
    pet_id: Optional[int] = None


class AdoptionIn(Schema):
    pet_id: int


class AdoptionOut(Schema):
    id: int
    customer_id: int
    pet_id: int
    solicitation_date: datetime.date
    status: str


class PetFilter(FilterSchema):
    id: Optional[int] = None
    

class PetIn(Schema):
    name: str
    species_id: int
    race: str
    age: int
    weight: Decimal
    description: str


class PetOut(Schema):
    id: int
    name: str
    species_id: int
    race: str
    age: int
    weight: Decimal
    description: str
    status: str
