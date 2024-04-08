import pytest
from constants import BAD_PASSWORD, TEST_EMAIL, TEST_PASSWORD
from fastapi import HTTPException
from sqlalchemy.orm import Session

from phoenix.auth import AdminAuth, User


@pytest.fixture
def auth_backend():
    # Create an instance of AdminAuth for testing
    return AdminAuth('test_secret_key')


@pytest.mark.asyncio
async def test_login_successful(auth_backend, mocker):
    # Mocking the request object
    request_mock = mocker.Mock()
    request_mock.form = mocker.AsyncMock(
        return_value={'username': TEST_EMAIL, 'password': TEST_PASSWORD},
    )

    # Mocking the session object
    session_mock = mocker.MagicMock(spec=Session)

    # Mocking the query result to return a user
    user_mock = mocker.MagicMock(spec=User)
    session_mock.query.return_value.filter.return_value.first.return_value = user_mock

    # Call the login method
    result = await auth_backend.login(request_mock)

    # Assert that login method returns True
    assert result is True

    # Assert that the session was updated with the token
    assert request_mock.session.update.called


@pytest.mark.asyncio
async def test_login_user_not_found(auth_backend, mocker):
    # Mocking the request object
    request_mock = mocker.Mock()
    request_mock.form = mocker.AsyncMock(
        return_value={'username': 'non_existent_user', 'password': 'test_password'},
    )

    # Mocking the session object
    session_mock = mocker.MagicMock(spec=Session)

    # Mocking the query result to return None (user not found)
    session_mock.query.return_value.filter.return_value.first.return_value = None

    # Call the login method and expect an HTTPException to be raised
    with pytest.raises(HTTPException) as exc_info:
        await auth_backend.login(request_mock)

    # Assert that HTTPException with status code 404 is raised
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_login_wrong_password(auth_backend, mocker):
    # Mocking the request object
    request_mock = mocker.Mock()
    request_mock.form = mocker.AsyncMock(
        return_value={'username': TEST_EMAIL, 'password': BAD_PASSWORD},
    )

    # Mocking the session object
    session_mock = mocker.MagicMock(spec=Session)

    # Mocking the query result to return a user
    user_mock = mocker.MagicMock(spec=User)
    session_mock.query.return_value.filter.return_value.first.return_value = user_mock

    # Mocking the verify_password function to return False
    mocker.patch('utils.verify_password', return_value=False)

    # Call the login method and expect an HTTPException to be raised
    with pytest.raises(HTTPException) as exc_info:
        await auth_backend.login(request_mock)

    # Assert that HTTPException with status code 403 is raised
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_logout_successful(auth_backend, mocker):
    # Mocking the request object
    request_mock = mocker.AsyncMock(session={'token': 'mocked_access_token'})

    # Call the logout method
    result = await auth_backend.logout(request_mock)

    # Assert that logout method returns True
    assert result is True

    # Assert that the session was cleared
    assert request_mock.session.clear


@pytest.mark.asyncio
@pytest.mark.parametrize('token', ['', 'mocked_access_token'])
async def test_authenticate_successful(auth_backend, token, mocker):
    # Mocking the request object
    request_mock = mocker.AsyncMock(session={'token': token})

    # Call the logout method
    result = await auth_backend.authenticate(request_mock)

    if token:
        # Assert that logout method returns True
        assert result is True

        # Assert that the session was cleared
        assert request_mock.session.clear
    else:
        assert result is False
