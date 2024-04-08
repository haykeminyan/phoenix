import os

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.environ.get('DATABASE_URL')

engine_prod = create_engine('postgresql+psycopg2://postgres:postgres@db:5432', echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_prod)


def init_db():
    SQLModel.metadata.create_all(engine_prod)


def get_session():
    with Session(engine_prod) as session:
        yield session
