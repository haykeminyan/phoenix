from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import EmailStr

from phoenix.models import ApartmentRent, ApartmentSale, User


class UserFilter(Filter):
    order_by: Optional[list[str]] = None
    email: Optional[EmailStr] = None
    id: Optional[int] = None
    is_active: Optional[bool] = None

    class Constants(Filter.Constants):
        model = User
        search_model_fields = [
            'email',
            'id',
            'is_active',
        ]  # It will search in both `name` and `email` columns.


class ApartmentBaseFilter(Filter):
    order_by: Optional[list[str]] = None
    living_area: Optional[int] = None
    living_area__lte: Optional[int] = None
    living_area__gte: Optional[int] = None
    number_of_bedrooms: Optional[int] = None
    number_of_bedrooms__lte: Optional[int] = None
    number_of_bedrooms__gte: Optional[int] = None
    number_of_bathrooms: Optional[int] = None
    number_of_bathrooms__lte: Optional[int] = None
    number_of_bathrooms__gte: Optional[int] = None
    building_year: Optional[int] = None
    building_year__lte: Optional[int] = None
    building_year__gte: Optional[int] = None
    condition: Optional[str] = None
    energy_label: Optional[str] = None


class ApartmentRentFilter(ApartmentBaseFilter):
    rent_price: Optional[int] = None
    rent_price__lte: Optional[int] = None
    rent_price__gte: Optional[int] = None

    class Constants(Filter.Constants):
        model = ApartmentRent


class ApartmentSaleFilter(Filter):
    sale_price: Optional[int] = None
    sale_price__lte: Optional[int] = None
    sale_price__gte: Optional[int] = None

    class Constants(Filter.Constants):
        model = ApartmentSale
