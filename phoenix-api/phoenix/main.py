import os
import re
import time
from typing import Annotated, List

import sentry_sdk
import uvicorn
from constants import (
    BAD_FIELDS_APARTMENT_RENT,
    BAD_FIELDS_APARTMENT_SALE,
    RENT_PATH_OUTPUT_TEMPLATE,
    RENT_PATH_TEMPLATE,
    SALE_PATH_OUTPUT_TEMPLATE,
    SALE_PATH_TEMPLATE,
)
from crud import (
    fill_rent_apartment,
    fill_sale_apartment,
    get_apartment,
    get_user_by_apartment_id,
    update_apartment,
    upload_image,
)
from db import SessionLocal, engine_prod
from docx import Document
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, Params, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_sqlalchemy import DBSessionMiddleware, db
from filters import ApartmentRentFilter, ApartmentSaleFilter, UserFilter
from parsing_docx import (
    ARRAY_OF_FIELDS_APARTMENT_RENT,
    ARRAY_OF_FIELDS_APARTMENT_SALE,
    docx_replace_one_regex,
)
from password_strength import PasswordPolicy
from schema import ApartmentRent as ApartmentRentSchema
from schema import ApartmentSale as ApartmentSaleSchema
from schema import CreateUser, UserOutput
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from sqladmin import Admin
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from starlette import status
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from utils import hash_pass, verify_password

from phoenix.admin import ApartmentRentAdmin, ApartmentSaleAdmin, UserAdmin
from phoenix.auth import AdminAuth
from phoenix.models import ApartmentRent as ApartmentRentModel
from phoenix.models import ApartmentSale as ApartmentSaleModel
from phoenix.models import User
from phoenix.validators import reject_bad_fields, reject_bad_fields_filtering

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

origins = [
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://localhost:4200',
    'http://127.0.0.1:4200',
    'http://192.168.65.1:4200',
    'http://192.168.65.1:8000'
]


sentry_sdk.init(
    dsn='https://f983fc46cf4947057d53473df44c6fee@o4506701381042176'
    '.ingest.sentry.io/4506701383008256',
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    enable_tracing=True,
    integrations=[
        StarletteIntegration(transaction_style='endpoint'),
        FastApiIntegration(transaction_style='endpoint'),
    ],
)


def create_app(env: str):
    app = FastAPI()
    app.add_middleware(DBSessionMiddleware, db_url=os.environ[env])
    app.add_middleware(SentryAsgiMiddleware)

    app.add_middleware(
        SessionMiddleware,
        secret_key=os.environ['SECRET_KEY'],
        max_age=int(os.environ['MAX_AGE']),
    )
    security = HTTPBasic()

    def check_user_is_authenticated(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    ):
        with SessionLocal() as session:
            user = session.query(User).filter(User.email == credentials.username).first()
            if not user:
                sentry_sdk.capture_exception(
                    HTTPException(status_code=404, detail='User is not found'),
                )
                raise HTTPException(status_code=404, detail='User is not found')

            if not verify_password(credentials.password, user.password):
                sentry_sdk.capture_exception(
                    HTTPException(status_code=403, detail='You have inputted the wrong password'),
                )
                raise HTTPException(status_code=403, detail='You have inputted the wrong password')

            user.credits -= 1

            if not user.is_active:
                sentry_sdk.capture_exception(
                    HTTPException(status_code=400, detail='You have been banned :=)'),
                )
                raise HTTPException(status_code=400, detail='You have been banned :=)')

            if user.credits < 0:
                sentry_sdk.capture_exception(
                    HTTPException(status_code=400, detail='Your credits are expired'),
                )
                raise HTTPException(status_code=400, detail='Your credits are expired')
            else:
                session.commit()
                session.refresh(user)
        return {'username': credentials.username, 'password': credentials.password, 'id': user.id}

    @app.get('/users', response_model=list[UserOutput])
    async def get_users(
        user_filter: UserFilter = FilterDepends(UserFilter),
        db: Session = Depends(get_db),
    ):
        query_filter = user_filter.filter(select(User))
        result = db.execute(query_filter)

        return result.scalars().all()

    def validate_password(password):
        policy = PasswordPolicy.from_names(
            length=8,  # min length: 8
            uppercase=1,  # need min. 2 uppercase letters
            numbers=1,  # need min. 2 digits
            special=1,  # need min. 2 special characters
            nonletters=1,  # need min. 2 non-letter characters (digits, specials, anything)
        )
        tested_pass = policy.password(password)

        # print(policy.test('V3ryG00dPassw0rd?!'))
        # # -> []  -- empty list means a good password
        # when empty list => everything is good and password is strong
        return not tested_pass.test()

    @app.post('/create_user', status_code=status.HTTP_201_CREATED, response_model=UserOutput)
    def create_users(user: CreateUser, db: Session = Depends(get_db)):
        # Hash The Password
        if not validate_password(user.password):
            sentry_sdk.capture_exception(
                HTTPException(status_code=400, detail='You password is weak, please change it'),
            )
            raise HTTPException(status_code=400, detail='You password is weak, please change it')

        hashed_pass = hash_pass(user.password)

        user.password = hashed_pass
        try:
            new_user = User(**user.model_dump())
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except IntegrityError:
            sentry_sdk.capture_exception(
                HTTPException(
                    status_code=403,
                    detail='User with this email is already registered',
                ),
            )
            raise HTTPException(
                status_code=403,
                detail='User with this email is already registered',
            )

        return new_user

    @app.post(
        '/apartment-sale/',
        response_model=ApartmentSaleSchema,
        status_code=status.HTTP_201_CREATED,
    )
    async def create_apartment_sale(
        apartment: ApartmentSaleSchema,
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        request: Request,
        files: List[UploadFile] = File(None),
    ):
        raw_body = request.state.raw_body
        reject_bad_fields(raw_body, BAD_FIELDS_APARTMENT_SALE)
        # Upload files
        uploaded_filenames = []
        await upload_image(files, uploaded_filenames, request)

        # Create apartment
        # Calculate coordinates if needed
        # if not apartment.latitude and not apartment.longitude:
        #     apartment.latitude = get_coordinates_throughout_address(apartment.address)[0]
        #     apartment.longitude = get_coordinates_throughout_address(apartment.address)[1]

        # Authenticate user

        current_user = check_user_is_authenticated(credentials)

        # Fill apartment data
        db_apartment = fill_sale_apartment(apartment)
        db_apartment.owner_id = current_user['id']

        # Add image filenames to apartment
        db_apartment.image = uploaded_filenames

        # Save apartment to database
        db.session.add(db_apartment)
        db.session.commit()

        return db_apartment

    @app.post(
        '/apartment-rent/',
        response_model=ApartmentRentSchema,
        status_code=status.HTTP_201_CREATED,
    )
    async def create_apartment_rent(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        apartment: ApartmentRentSchema,
        request: Request,
        files: List[UploadFile] = File(None),
    ):
        raw_body = request.state.raw_body
        reject_bad_fields(raw_body, BAD_FIELDS_APARTMENT_RENT)

        print('!'*1000)
        # Upload files
        uploaded_filenames = []
        await upload_image(files, uploaded_filenames, request)

        # Create apartment
        # Calculate coordinates if needed
        # if not apartment.latitude and not apartment.longitude:
        #     apartment.latitude = get_coordinates_throughout_address(apartment.address)[0]
        #     apartment.longitude = get_coordinates_throughout_address(apartment.address)[1]

        current_user = check_user_is_authenticated(credentials)
        # Fill apartment data
        db_apartment = fill_rent_apartment(apartment)
        db_apartment.owner_id = current_user['id']

        # Add image filenames to apartment
        db_apartment.image = uploaded_filenames
        # Save apartment to database
        db.session.add(db_apartment)
        db.session.commit()

        return db_apartment
        # else:
        #     return {"message": f"Successfully uploaded {uploaded_filenames}"}

    @app.put(
        '/apartment-rent/{rent_id}',
        response_model=ApartmentRentSchema,
        status_code=status.HTTP_200_OK,
    )
    async def edit_apartment_rent(
        rent_id: int,
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        apartment: ApartmentRentSchema,
        request: Request,
        files: List[UploadFile] = File(None),
        db: Session = Depends(get_db),
    ):
        check_user_is_authenticated(credentials)
        uploaded_filenames = []
        await upload_image(files, uploaded_filenames, request)
        db_apartment = update_apartment(ApartmentRentModel, rent_id, apartment, db)
        db_apartment.image = uploaded_filenames
        db.add(db_apartment)
        db.commit()
        return db_apartment

    @app.put(
        '/apartment-sale/{sale_id}',
        response_model=ApartmentSaleSchema,
        status_code=status.HTTP_200_OK,
    )
    async def edit_apartment_sale(
        sale_id: int,
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        apartment: ApartmentSaleSchema,
        request: Request,
        files: List[UploadFile] = File(None),
        db: Session = Depends(get_db),
    ):
        check_user_is_authenticated(credentials)
        uploaded_filenames = []
        await upload_image(files, uploaded_filenames, request)
        db_apartment = update_apartment(ApartmentSaleModel, sale_id, apartment, db)
        db_apartment.image = uploaded_filenames
        db.add(db_apartment)
        db.commit()
        return db_apartment

    @app.get(
        '/apartment-rent/{rent_id}',
        response_model=ApartmentRentSchema,
        status_code=status.HTTP_200_OK,
    )
    def get_apartment_rent(
        rent_id: int,
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        db: Session = Depends(get_db),
    ):
        check_user_is_authenticated(credentials)
        return get_apartment(rent_id, ApartmentRentModel, db)

    @app.get(
        '/apartment-sale/{sale_id}',
        response_model=ApartmentSaleSchema,
        status_code=status.HTTP_200_OK,
    )
    def get_apartment_sale(
        sale_id: int,
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        db: Session = Depends(get_db),
    ):
        check_user_is_authenticated(credentials)
        return get_apartment(sale_id, ApartmentSaleModel, db)

    @app.get(
        '/all-apartment-sale/',
        response_model=Page[ApartmentSaleSchema],
        status_code=status.HTTP_200_OK,
    )
    def get_all_apartment_sale(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        request: Request,
        apartment_filter: ApartmentSaleFilter = FilterDepends(ApartmentSaleFilter),
        db: Session = Depends(get_db),
        size: int = 10,
        page: int = 1,
    ):
        check_user_is_authenticated(credentials)
        reject_bad_fields_filtering(request.url, BAD_FIELDS_APARTMENT_SALE)
        query = apartment_filter.filter(select(ApartmentSaleModel))
        params = Params(size=size, page=page)
        return paginate(db, query, params)

    @app.get(
        '/all-apartment-rent/',
        response_model=Page[ApartmentRentSchema],
        status_code=status.HTTP_200_OK,
    )
    def get_all_apartment_rent(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        request: Request,
        apartment_filter: ApartmentRentFilter = FilterDepends(ApartmentRentFilter),
        db: Session = Depends(get_db),
        size: int = 10,
        page: int = 1,
    ):
        check_user_is_authenticated(credentials)
        reject_bad_fields_filtering(request.url, BAD_FIELDS_APARTMENT_RENT)
        query = apartment_filter.filter(select(ApartmentRentModel))
        params = Params(size=size, page=page)
        return paginate(db, query, params)

    @app.delete(
        '/apartment-rent/{rent_id}',
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def delete_apartment_rent(
        rent_id: int,
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        db: Session = Depends(get_db),
    ):
        check_user_is_authenticated(credentials)
        db_apartment = get_apartment(rent_id, ApartmentRentModel, db)
        db.delete(db_apartment)
        db.commit()

    @app.delete(
        '/apartment-sale/{sale_id}',
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def delete_apartment_sale(
        sale_id: int,
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        db: Session = Depends(get_db),
    ):
        check_user_is_authenticated(credentials)
        db_apartment = get_apartment(sale_id, ApartmentSaleModel, db)
        db.delete(db_apartment)
        db.commit()

    @app.get(
        '/doc/apartment-sale/{apartment_id}',
        status_code=status.HTTP_200_OK,
        response_class=FileResponse,
    )
    def get_sale_template(
        apartment_id: int,
        creditionals: Annotated[HTTPBasicCredentials, Depends(security)],
        db: Session = Depends(get_db),
    ):
        check_user_is_authenticated(creditionals)
        doc = Document(SALE_PATH_TEMPLATE)
        apartment = get_apartment(apartment_id, ApartmentSaleModel, db)
        user = get_user_by_apartment_id(apartment_id, ApartmentSaleModel, db)
        apartment.__dict__['email'] = user.email

        for field in ARRAY_OF_FIELDS_APARTMENT_SALE:
            docx_replace_one_regex(doc, re.compile(rf'^{field}$'), apartment.__dict__[field])

        filename = SALE_PATH_OUTPUT_TEMPLATE.replace('number', str(apartment_id))
        doc.save(filename)
        return FileResponse(filename, filename=filename)

    @app.get(
        '/doc/apartment-rent/{apartment_id}',
        status_code=status.HTTP_200_OK,
        response_class=FileResponse,
    )
    def get_rent_template(
        apartment_id: int,
        creditionals: Annotated[HTTPBasicCredentials, Depends(security)],
        db: Session = Depends(get_db),
    ):
        check_user_is_authenticated(creditionals)
        doc = Document(RENT_PATH_TEMPLATE)
        apartment = get_apartment(apartment_id, ApartmentRentModel, db)
        user = get_user_by_apartment_id(apartment_id, ApartmentRentModel, db)
        apartment.__dict__['email'] = user.email

        for field in ARRAY_OF_FIELDS_APARTMENT_RENT:
            docx_replace_one_regex(doc, re.compile(rf'^{field}$'), apartment.__dict__[field])

        filename = RENT_PATH_OUTPUT_TEMPLATE.replace('number', str(apartment_id))
        doc.save(filename)
        return FileResponse(filename, filename=filename)

    return app


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine_prod)


app = create_app('DATABASE_URL')
app.mount('/templates/images', StaticFiles(directory='templates/images'), name='static')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['*'],
)
authentication_backend = AdminAuth(secret_key=os.environ['SECRET_KEY'])
admin = Admin(app, engine_prod, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(ApartmentSaleAdmin)
admin.add_view(ApartmentRentAdmin)
add_pagination(app)


@app.on_event('startup')
def on_startup():
    create_db_and_tables()


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


@app.middleware('http')
async def raw_body_middleware(request: Request, call_next):
    if request.method == 'POST':
        body = await request.body()
        request.state.raw_body = str(body)
    response = await call_next(request)
    return response


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
