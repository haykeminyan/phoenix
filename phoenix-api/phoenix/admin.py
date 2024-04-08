from sqladmin import ModelView

from phoenix.models import ApartmentRent, ApartmentSale, User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.credits]


class ApartmentSaleAdmin(ModelView, model=ApartmentSale):
    column_list = [ApartmentSale.id]


class ApartmentRentAdmin(ModelView, model=ApartmentRent):
    column_list = [ApartmentRent.id]
