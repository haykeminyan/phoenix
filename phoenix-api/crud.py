import re
import uuid
from typing import List

import sentry_sdk
from fastapi import HTTPException, UploadFile
from pydantic import BaseModel
from schema import ApartmentRent as ApartmentRentSchema
from schema import ApartmentSale as ApartmentSaleSchema
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from phoenix.models import ApartmentRent as ApartmentRentModel
from phoenix.models import ApartmentSale as ApartmentSaleModel
from phoenix.models import Base, User


def get_apartment(apartment_id: int, model: Base, db: Session):
    obj = db.query(model).filter_by(id=apartment_id).first()
    if obj is None:
        sentry_sdk.capture_exception(
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Apartment is not found',
            ),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Apartment is not found',
        )
    return obj


def get_user_by_apartment_id(apartment_id: int, model: Base, db: Session):
    obj = get_apartment(apartment_id, model, db)
    user = db.query(User).filter_by(id=obj.__dict__['owner_id']).first()

    if user is None:
        sentry_sdk.capture_exception(
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User is not found',
            ),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User is not found',
        )
    return user


def update_apartment(model: Base, apartment_id: int, schema: BaseModel, db: Session):
    current_apartment = db.query(model).filter_by(id=apartment_id).first()
    if not current_apartment:
        raise HTTPException(status_code=404, detail='Apartment is not found')
    else:
        current_apartment.living_area = schema.living_area
        current_apartment.latitude = schema.latitude
        current_apartment.longitude = schema.longitude
        current_apartment.condition = schema.condition
        current_apartment.energy_label = schema.energy_label
        current_apartment.number_of_bedrooms = schema.number_of_bedrooms
        current_apartment.number_of_bathrooms = schema.number_of_bathrooms
        current_apartment.building_year = schema.building_year
        current_apartment.address = schema.address
        current_apartment.image = schema.image

        if model == ApartmentRentModel:
            current_apartment.rent_price = schema.rent_price
        elif model == ApartmentSaleModel:
            current_apartment.sale_price = schema.sale_price

    return current_apartment


def get_all_apartment(model: Base):
    return select(model).order_by(model.id)


def fill_rent_apartment(apartment: ApartmentRentSchema):
    return ApartmentRentModel(**apartment.model_dump())


def fill_sale_apartment(apartment: ApartmentSaleSchema):
    return ApartmentSaleModel(**apartment.model_dump())


# TODO need to add possibility uploading more than 1 picture
async def upload_image(files: List[UploadFile], uploaded_filenames: List[str], request: Request):
    if files:
        for file in files:
            try:
                # Read the file contents once and save it
                contents = await file.read()
                file.extension = re.search('(.\w+)$', str(file.filename)).group(1)
                unique_filename = str(uuid.uuid4())
                # file.filename = image_name
                filename = f'templates/images/{unique_filename}{file.extension}'
                with open(filename, 'wb') as f:
                    f.write(contents)
                uploaded_filenames.append(filename)
            except Exception:
                return {'message': 'There was an error uploading the file(s)'}
    else:
        if 'apartment-rent' in str(request.url):
            filename = 'templates/images/default/apartment-rent-default.jpg'
            uploaded_filenames.append(filename)
        elif 'apartment-sale' in str(request.url):
            filename = 'templates/images/default/apartment-sale-default.jpg'
            uploaded_filenames.append(filename)
