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
    customer_name: str
    pet_id: int
    pet_name: str
    solicitation_date: datetime.date
    status: str
    
    @staticmethod
    def resolve_customer_name(obj):
        return obj.customer.get_full_name()
    
    @staticmethod
    def resolve_pet_name(obj):
        return obj.pet.name
    
    @staticmethod
    def resolve_status(obj):
        return obj.get_status_display()


class PetFilter(FilterSchema):
    id: Optional[int] = None
    status: Optional[str] = None
    

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
    species_name: str
    race: str
    age: int
    weight: Decimal
    description: str
    status: str
    
    @staticmethod
    def resolve_species_name(obj):
        return obj.species.name
