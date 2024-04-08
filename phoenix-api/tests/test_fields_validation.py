import json

import pytest
from constants import (
    CREATE_APARTMENT_RENT,
    CREATE_APARTMENT_SALE,
    TEST_EMAIL,
    TEST_PASSWORD,
)
from enums import Condition
from fastapi.testclient import TestClient
from mocked_data import MOCKED_APARTMENT_RENT, MOCKED_APARTMENT_SALE
from requests.auth import _basic_auth_str


@pytest.mark.parametrize(
    'living_area',
    [123, '', None],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__validation_living_area(client: TestClient, living_area, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['living_area'] = living_area
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request_sale = client.post(
        endpoint,
        data=json.loads(mock_res),
        headers={'Authorization': payload},
    )

    # then
    if isinstance(living_area, int):
        assert request_sale.status_code == 201
        assert request_sale.json()['living_area'] == 123
    else:
        assert request_sale.status_code == 422
        assert 'should be a valid integer' in request_sale.json()['detail'][0]['msg']


@pytest.mark.parametrize(
    'number_of_bedrooms',
    [2, 'foo'],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__validation_number_of_bedrooms(client: TestClient, number_of_bedrooms, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['number_of_bedrooms'] = number_of_bedrooms
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request = client.post(endpoint, data=json.loads(mock_res), headers={'Authorization': payload})

    # then
    if isinstance(number_of_bedrooms, int):
        assert request.status_code == 201
        assert request.json()['number_of_bedrooms'] == 2
    else:
        assert request.status_code == 422
        assert 'valid integer' in request.json()['detail'][0]['msg']


@pytest.mark.parametrize(
    'number_of_bathrooms',
    ['', 2],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__validation_number_of_bathrooms(client: TestClient, number_of_bathrooms, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['number_of_bathrooms'] = number_of_bathrooms
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request_sale = client.post(
        endpoint,
        data=json.loads(mock_res),
        headers={'Authorization': payload},
    )

    # then
    if isinstance(number_of_bathrooms, int):
        assert request_sale.status_code == 201
        assert request_sale.json()['number_of_bathrooms'] == 2
    else:
        assert request_sale.status_code == 422
        assert 'valid integer' in request_sale.json()['detail'][0]['msg']


@pytest.mark.parametrize(
    'condition',
    [2, 'good', None, 'foo'],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__validation_condition(client: TestClient, condition, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['condition'] = condition
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request_sale = client.post(
        endpoint,
        data=json.loads(mock_res),
        headers={'Authorization': payload},
    )

    # then
    if isinstance(condition, str):
        if condition in [Condition.GOOD, Condition.SECOND_HAND, Condition.NEED_RENOVATION]:
            assert request_sale.status_code == 201
            assert request_sale.json()['condition'] == 'good'
        else:
            assert request_sale.status_code == 422
            assert 'should be \'good\'' in request_sale.json()['detail'][0]['msg']
    else:
        assert request_sale.status_code == 422
        assert 'valid string' in request_sale.json()['detail'][0]['msg']


@pytest.mark.parametrize(
    'energy_label',
    [12, 'a'],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__validation_energy_label(client: TestClient, energy_label, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['energy_label'] = energy_label
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request_sale = client.post(
        endpoint,
        data=json.loads(mock_res),
        headers={'Authorization': payload},
    )

    # then
    if isinstance(energy_label, str):
        assert request_sale.status_code == 201
        assert request_sale.json()['energy_label'] == 'a'
    else:
        assert request_sale.status_code == 422
        assert 'valid string' in request_sale.json()['detail'][0]['msg']


@pytest.mark.parametrize(
    'building_year',
    ['a', 1996],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__validation_building_year(client: TestClient, building_year, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['building_year'] = building_year
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request_sale = client.post(
        endpoint,
        data=json.loads(mock_res),
        headers={'Authorization': payload},
    )

    # then
    if isinstance(building_year, int):
        assert request_sale.status_code == 201
        assert request_sale.json()['building_year'] == 1996
    else:
        assert request_sale.status_code == 422
        assert 'valid integer' in request_sale.json()['detail'][0]['msg']


@pytest.mark.parametrize(
    'latitude',
    ['!@#', 40.151],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__validation_latitude(client: TestClient, latitude, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['latitude'] = latitude
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request_sale = client.post(
        endpoint,
        data=json.loads(mock_res),
        headers={'Authorization': payload},
    )

    # then
    if isinstance(latitude, float):
        assert request_sale.status_code == 201
        assert request_sale.json()['latitude'] == 40.151
    else:
        assert request_sale.status_code == 422
        assert 'valid number' in request_sale.json()['detail'][0]['msg']


@pytest.mark.parametrize(
    'longitude',
    ['fd', 44.516],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__validation_longitude(client: TestClient, longitude, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['longitude'] = longitude
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request_sale = client.post(
        endpoint,
        data=json.loads(mock_res),
        headers={'Authorization': payload},
    )

    # then
    if isinstance(longitude, float):
        assert request_sale.status_code == 201
        assert request_sale.json()['longitude'] == 44.516
    else:
        assert request_sale.status_code == 422
        assert 'valid number' in request_sale.json()['detail'][0]['msg']


@pytest.mark.parametrize(
    'sale_price',
    ['foo'],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    ([CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],),
)
def test__validation_sale_price(client: TestClient, sale_price, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['sale_price'] = sale_price
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request_sale = client.post(
        endpoint,
        data=json.loads(mock_res),
        headers={'Authorization': payload},
    )

    # then
    assert request_sale.status_code == 422
    assert 'valid integer' in request_sale.json()['detail'][0]['msg']


@pytest.mark.parametrize(
    'rent_price',
    ['boo'],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    ([CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],),
)
def test__validation_rent_price(client: TestClient, rent_price, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['rent_price'] = rent_price
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request_sale = client.post(
        endpoint,
        data=json.loads(mock_res),
        headers={'Authorization': payload},
    )

    # then
    assert request_sale.status_code == 422
    assert 'valid integer' in request_sale.json()['detail'][0]['msg']


@pytest.mark.parametrize(
    'address',
    [123, 'Erebuni, Yerevan, street Muratsan'],
)
@pytest.mark.parametrize(
    'endpoint, mock',
    (
        [CREATE_APARTMENT_SALE, MOCKED_APARTMENT_SALE],
        [CREATE_APARTMENT_RENT, MOCKED_APARTMENT_RENT],
    ),
)
def test__validation_address(client: TestClient, address, endpoint, mock):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    mock_json = json.loads(mock['apartment'])
    mock_json['address'] = address
    mock_res = json.dumps({'apartment': json.dumps(mock_json)})

    # when
    request_sale = client.post(
        endpoint,
        data=json.loads(mock_res),
        headers={'Authorization': payload},
    )

    # then
    if isinstance(address, str):
        assert request_sale.status_code == 201
        assert request_sale.json()['address'] == 'Erebuni, Yerevan, street Muratsan'
    else:
        assert request_sale.status_code == 422
        assert 'valid string' in request_sale.json()['detail'][0]['msg']
