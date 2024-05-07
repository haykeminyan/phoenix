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
    id: int | None = Field(default=None)
    living_area: int
    number_of_bedrooms: int | None = None
    number_of_bathrooms:  int | None = None
    condition: Condition
    energy_label: EnergyLabel | None = None
    building_year: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: str = Field(..., description="Address of the apartment")
    # create new class and list[Image] | None = None
    image: str | None = None
    owner_id: int | None = Field(default=None, foreign_key='users.id')

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
