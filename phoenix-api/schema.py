import json
from typing import Optional

from enums import Condition, EnergyLabel
from pydantic import BaseModel, EmailStr, Field, model_validator


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    email: EmailStr
    id: int

    class Config:
        orm_mode = True


class Apartment(BaseModel):
    id: Optional[int] = Field(default=None)
    living_area: int
    number_of_bedrooms: Optional[int] = None
    number_of_bathrooms: Optional[int] = None
    condition: Condition = Field(...)
    energy_label: Optional[EnergyLabel] = None
    building_year: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: str = Field(...)
    # create new class and list[Image] | None = None
    image: Optional[str] = None
    owner_id: Optional[int] = Field(default=None, foreign_key='users.id')

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    class Config:
        orm_mode = True


class ApartmentSale(Apartment):
    sale_price: Optional[int]


class ApartmentRent(Apartment):
    rent_price: Optional[int]
