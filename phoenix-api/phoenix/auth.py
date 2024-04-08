import sentry_sdk
from db import SessionLocal
from fastapi import HTTPException
from fastapi_jwt import JwtAccessBearer
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from utils import verify_password

from phoenix.models import User

access_security = JwtAccessBearer(secret_key='secret_key', auto_error=True)


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get('username'), form.get('password')
        with SessionLocal() as session:
            user = session.query(User).filter(User.email == username).first()

            if not user:
                sentry_sdk.capture_exception(
                    HTTPException(status_code=404, detail='User is not found'),
                )
                raise HTTPException(status_code=404, detail='User is not found')

            if not verify_password(password, user.password):
                sentry_sdk.capture_exception(
                    HTTPException(status_code=403, detail='You have inputted the wrong password'),
                )
                raise HTTPException(status_code=403, detail='You have inputted the wrong password')

            subject = {'username': f'{User.email}'}

            if user:
                request.session.update(
                    {'token': access_security.create_access_token(subject=subject)},
                )
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get('token')

        if not token:
            return False

        return True
