import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from phoenix.main import add_process_time_header, raw_body_middleware


def test__exist_add_process_time_header(client: TestClient):
    # when
    response = client.get('/users')
    assert response.status_code == 200
    assert 'X-Process-Time' in response.headers
    process_time = float(response.headers['X-Process-Time'])
    assert process_time >= 0


class MockResponse:
    def __init__(self, headers):
        self.headers = headers


async def mock_call_next(request):
    # Mock implementation of the next middleware or request handler
    return MockResponse(headers={})


@pytest.mark.asyncio
async def test_add_process_time_header(mocker):
    # Mock the Request object
    request_mock = mocker.Mock(spec=Request)

    # Mock the call_next function
    await mock_call_next(request=Request)

    # Call the middleware function
    response = await add_process_time_header(request_mock, mock_call_next)

    # Assert that the X-Process-Time header is added to the response
    assert 'X-Process-Time' in response.headers
    assert isinstance(float(response.headers['X-Process-Time']), float)


@pytest.mark.asyncio
async def test_raw_body_middleware(mocker):
    # Mock the Request object
    request_mock = mocker.Mock(spec=Request)

    # Mock the call_next function
    await mock_call_next(request=Request)

    # Mock the body method of the request object to return a dictionary
    request_mock.body.return_value = "{'key': 'value'}"

    # Create a MagicMock for the raw_body attribute
    raw_body_mock = mocker.MagicMock(return_value="{'key': 'value'}")

    # Set the raw_body attribute of the request state to the MagicMock
    request_mock.state.raw_body = raw_body_mock

    # Assert that the request body was correctly processed and raw_body was set
    assert hasattr(request_mock.state, 'raw_body')

    # Assert that the return value of the mocked raw_body attribute matches the expected dictionary
    assert request_mock.state.raw_body() == str(request_mock.body.return_value)
