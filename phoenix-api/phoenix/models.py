from datetime import date, datetime

import pytz
import json
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Time, ARRAY,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


tz = pytz.timezone('Europe/Lisbon')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_date = Column(Date, default=date.today())
    created_time = Column(Time, default=datetime.now(tz))
    credits = Column(Integer, default=5)


class Apartment(Base):
    __abstract__ = True
    id = Column('id', Integer, primary_key=True, index=True)
    image = Column('image', Text)
    living_area = Column('living_area', Integer)
    # T-{number} this is number_of_bedrooms
    number_of_bedrooms = Column('number_of_bedrooms', Integer)
    number_of_bathrooms = Column('number_of_bathrooms', Integer)
    address = Column('address', Text)
    condition = Column('condition', Text)
    energy_label = Column('energy_label', Text)
    building_year = Column('building_year', Integer)
    latitude = Column('latitude', Float)
    longitude = Column('longitude', Float)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'))


class ApartmentSale(Apartment):
    __tablename__ = 'apartments_sale'
    sale_price = Column('sale_price', Integer)


class ApartmentRent(Apartment):
    __tablename__ = 'apartments_rent'
    rent_price = Column('rent_price', Integer)
