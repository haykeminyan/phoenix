from unittest.mock import MagicMock

import pytest
from constants import (
    BAD_EMAIL,
    BAD_PASSWORD,
    CREATE_APARTMENT_RENT,
    CREATE_APARTMENT_SALE,
    CREATE_USER_URL,
    FAKE_EMAIL,
    IS_ACTIVE,
    IS_BANNED,
    LIST_USERS,
    MILLION_CREDITS,
    TEST_EMAIL,
    TEST_PASSWORD,
    ZERO_CREDITS,
)
from crud import get_apartment, get_user_by_apartment_id, upload_image
from db import SessionLocal
from fastapi import HTTPException
from fastapi.testclient import TestClient
from mocked_data import MOCKED_APARTMENT_RENT, MOCKED_APARTMENT_SALE
from random_word import RandomWords
from requests.auth import _basic_auth_str
from starlette.requests import Request
from utils import hash_pass

from phoenix.models import ApartmentRent, ApartmentSale, User


# Test which describes creating user and validates passwords with email
@pytest.mark.parametrize(
    'email, password',
    [
        (TEST_EMAIL, TEST_PASSWORD),
        (TEST_EMAIL, BAD_PASSWORD),
        (BAD_EMAIL, TEST_PASSWORD),
    ],
)
def test__create_users_bad_cases(client: TestClient, email, password):
    # given
    payload = {'email': email, 'password': password}

    # when
    request = client.post(CREATE_USER_URL, json=payload)

    # then
    if email == TEST_EMAIL and password == TEST_PASSWORD:
        assert request.status_code == 403
        assert request.json()['detail'] == 'User with this email is already registered'

    elif email == BAD_EMAIL:
        assert request.status_code == 422
        assert 'value is not a valid email address' in request.json()['detail'][0]['msg']

    elif password == BAD_PASSWORD:
        assert request.status_code == 400
        assert request.json()['detail'] == 'You password is weak, please change it'


@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
@pytest.mark.parametrize(
    'is_active, credits',
    [
        (IS_ACTIVE, ZERO_CREDITS),
        (IS_BANNED, MILLION_CREDITS),
        (IS_BANNED, ZERO_CREDITS),
    ],
)
def test__create_users_active_credits(
    client: TestClient,
    mock,
    is_active,
    credits,
    endpoint,
    session,
):
    # given
    r = RandomWords()
    email = f'{r.get_random_word()}@gmail.com'
    payload = {'email': email, 'password': TEST_PASSWORD}

    # when
    request_create_user = client.post(CREATE_USER_URL, json=payload)

    with SessionLocal() as session:
        user = (
            session.query(User).filter(User.email == request_create_user.json()['email']).first()
        )
        user.is_active = is_active
        user.credits = credits
        session.commit()

        request_create_property = client.post(
            endpoint,
            data=mock,
            headers={'Authorization': _basic_auth_str(user.email, TEST_PASSWORD)},
        )

        # then
        if is_active == IS_ACTIVE and credits == ZERO_CREDITS:
            assert request_create_property.status_code == 400
            assert request_create_property.json()['detail'] == 'Your credits are expired'

        elif is_active == IS_BANNED and credits == MILLION_CREDITS:
            assert request_create_property.status_code == 400
            assert request_create_property.json()['detail'] == 'You have been banned :=)'

        elif is_active == IS_BANNED and credits == ZERO_CREDITS:
            assert request_create_property.status_code == 400
            assert request_create_property.json()['detail'] == 'You have been banned :=)'

        session.delete(user)
        session.commit()


@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__auth_bad_password(client: TestClient, mock, endpoint, session):
    # given
    r = RandomWords()
    email = f'{r.get_random_word()}@gmail.com'
    payload = {'email': email, 'password': TEST_PASSWORD}

    # when
    request_create_user = client.post(CREATE_USER_URL, json=payload)

    with SessionLocal() as session:
        user = (
            session.query(User).filter(User.email == request_create_user.json()['email']).first()
        )
        hashed_pass = hash_pass(user.password)
        user.password = hashed_pass
        session.commit()

        request_create_property = client.post(
            endpoint,
            data=mock,
            headers={'Authorization': _basic_auth_str(user.email, TEST_PASSWORD)},
        )

        # then
        assert request_create_property.status_code == 403
        assert request_create_property.json()['detail'] == 'You have inputted the wrong password'

        session.delete(user)
        session.commit()


@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__auth_user_not_exist(client: TestClient, mock, endpoint):
    # when
    request_create_property = client.post(
        endpoint,
        data=mock,
        headers={'Authorization': _basic_auth_str(FAKE_EMAIL, TEST_PASSWORD)},
    )

    assert request_create_property.status_code == 404
    assert request_create_property.json()['detail'] == 'User is not found'


def test__list_users(client: TestClient):
    # when
    request_users = client.get(
        LIST_USERS,
        headers={'Authorization': _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)},
    )

    assert request_users.status_code == 200


@pytest.mark.parametrize(
    'endpoint, mock, model',
    (
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT, ApartmentRent],
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE, ApartmentSale],
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE, ApartmentSale],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT, ApartmentRent],
    ),
)
def test__get_user_by_apartment_id(client: TestClient, endpoint, mock, mocker, model, session):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    files = [
        ('files', ('apartment.png', open('tests/templates/apartment.png', 'rb'), 'image/png')),
    ]

    # when
    request = client.post(
        endpoint,
        data=mock,
        headers={'Authorization': payload},
        files=files,
    )

    # then
    assert request.status_code == 201

    apartment_id = request.json()['id']

    with SessionLocal() as session:
        user = get_user_by_apartment_id(apartment_id, model, session)
        assert user.email == TEST_EMAIL

        with pytest.raises(HTTPException) as exc_info:
            get_apartment(apartment_id=-100, model=ApartmentSale, db=session)
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == 'Apartment is not found'

        session_mock = mocker.Mock(spec=session)

        # Mocking the query method of the session to return a query object
        query_mock = session_mock.query.return_value

        # Mocking the filter_by method of the query object to return another query object
        filter_by_mock = query_mock.filter_by.return_value

        # Mocking the first method of the filtered query object to return None
        filter_by_mock.first.return_value = None

        # Mocking the get_apartment function to simulate no apartment found
        mocker.patch('crud.get_apartment', side_effect=mock_get_apartment)

        with pytest.raises(HTTPException) as exc_info:
            get_user_by_apartment_id(
                apartment_id=apartment_id,
                model=ApartmentSale,
                db=session_mock,
            )
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == 'User is not found'


def mock_get_apartment(apartment_id, model, db):
    # Mock implementation of get_apartment for testing purposes
    # Return an object with owner_id attribute
    class MockApartment:
        def __init__(self, owner_id):
            self.owner_id = owner_id

    return MockApartment(owner_id=1)


@pytest.mark.asyncio
async def test__bad_image():
    # Mocking a file object with a side effect to raise an exception
    files = [MagicMock(filename='test.png', read=MagicMock(side_effect=Exception('Test error')))]
    request = MagicMock(spec=Request)
    # Mocking the uploaded_filenames list
    uploaded_filenames = []

    # Call the function
    response = await upload_image(files, uploaded_filenames, request)

    # Assert that the function returns the error message
    assert response == {'message': 'There was an error uploading the file(s)'}
    assert len(uploaded_filenames) == 0  # Assert that no filenames were appended due to error


@pytest.mark.parametrize(
    'url, default_image, mock',
    (
        [
            CREATE_APARTMENT_SALE,
            '{templates/images/default/apartment-sale-default.jpg}',
            MOCKED_APARTMENT_SALE,
        ],
        [
            CREATE_APARTMENT_RENT,
            '{templates/images/default/apartment-rent-default.jpg}',
            MOCKED_APARTMENT_RENT,
        ],
    ),
)
def test__default_image(client: TestClient, url, default_image, mock):
    # Mocking a file object with a side effect to raise an exception
    request_create_property = client.post(
        url,
        data=mock,
        headers={'Authorization': _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)},
    )

    # Call the function
    assert request_create_property.json()['image'] == default_image
