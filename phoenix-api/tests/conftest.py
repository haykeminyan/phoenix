import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from phoenix.main import create_app

app = create_app('DATABASE_TEST_URL')
engine_test = create_engine('postgresql+psycopg2://postgres:postgres@db-test/postgres', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def init_db():
    SQLModel.metadata.create_all(engine_test)


def get_session():
    with Session(engine_test) as session:
        yield session


class AddProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        return response


class RawBodyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == 'POST':
            body = await request.body()
            request.state.raw_body = str(body)
        response = await call_next(request)
        return response


app.add_middleware(AddProcessTimeHeaderMiddleware)  # Add middleware before starting the app
app.add_middleware(RawBodyMiddleware)


@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine(
        'postgresql+psycopg2://postgres:postgres@db-test/postgres',
        echo=True,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name='client')
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    #
    yield client
    app.dependency_overrides.clear()
