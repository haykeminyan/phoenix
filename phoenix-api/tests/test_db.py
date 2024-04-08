import pytest
from db import engine_prod, get_session, init_db
from sqlmodel import SQLModel

from phoenix.main import create_db_and_tables, on_startup
from phoenix.models import ApartmentRent, ApartmentSale


def test_on_startup(mocker):
    # Mock the create_db_and_tables function
    create_db_and_tables_mock = mocker.patch('phoenix.main.create_db_and_tables')

    # Call the on_startup function
    on_startup()

    # Assert that the create_db_and_tables function was called once
    create_db_and_tables_mock.assert_called_once()


def test__init_db():
    # Import the init_db function from your module
    init_db()
    # Add assertions to verify that the database initialization was successful


def test__get_session():
    # Import the get_session function from your module
    session_generator = get_session()
    # Obtain a session from the generator
    # Add assertions to verify that the session is valid and usable
    assert next(session_generator)


def test_client_fixture(client):
    """
    Test the client fixture.
    """
    # Perform assertions or test the behavior of the client fixture
    # For example, you can check if the client has access to the overridden session
    assert True


@pytest.mark.parametrize('model', [ApartmentSale, ApartmentRent])
def test__session_fixture(session, model):
    # Write test cases using the session fixture
    assert session.query(model).count() > 0  # Example assertion


def test_create_db_and_tables(mocker):
    # Mock SQLModel.metadata.create_all method
    create_all_mock = mocker.patch.object(SQLModel.metadata, 'create_all')

    # Call the function
    create_db_and_tables()

    # Assert that SQLModel.metadata.create_all method was called once with the correct arguments
    create_all_mock.assert_called_once_with(engine_prod)
