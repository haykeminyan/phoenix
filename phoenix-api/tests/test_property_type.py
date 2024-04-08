import pytest
import sqlalchemy
from constants import (
    CREATE_APARTMENT_RENT,
    CREATE_APARTMENT_SALE,
    GET_APARTMENT_RENT,
    GET_APARTMENT_RENT_QUERY,
    GET_APARTMENT_SALE,
    GET_APARTMENT_SALE_QUERY,
    TEST_EMAIL,
    TEST_PASSWORD,
)
from crud import get_all_apartment
from fastapi.testclient import TestClient
from mocked_data import (
    EDITED_MOCKED_APARTMENT_RENT,
    EDITED_MOCKED_APARTMENT_SALE,
    MOCKED_APARTMENT_RENT,
    MOCKED_APARTMENT_SALE,
)
from requests.auth import _basic_auth_str

from phoenix.models import ApartmentRent, ApartmentSale


# User check if sale apartment is created
def test__apartment_sale(client: TestClient):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    files = [
        ('files', ('apartment.png', open('tests/templates/apartment.png', 'rb'), 'image/png')),
    ]
    # when
    request_sale = client.post(
        CREATE_APARTMENT_SALE,
        data=MOCKED_APARTMENT_SALE,
        headers={'Authorization': payload},
        files=files,
    )

    # then
    assert request_sale.status_code == 201
    assert request_sale.json()['living_area'] == 123
    assert request_sale.json()['number_of_bedrooms'] == 2
    assert request_sale.json()['number_of_bathrooms'] == 2
    assert request_sale.json()['condition'] == 'good'
    assert request_sale.json()['energy_label'] == 'a'
    assert request_sale.json()['building_year'] == 1996
    assert request_sale.json()['latitude'] == 40.151
    assert request_sale.json()['longitude'] == 44.516
    assert request_sale.json()['address'] == 'Erebuni, Yerevan, street Muratsan'
    assert request_sale.json()['sale_price'] == 123000
    assert request_sale.json()['image'] == '{templates/images/apartment.png}'

    request_show_all = client.get(
        GET_APARTMENT_SALE_QUERY,
        headers={'Authorization': payload},
    )
    assert request_show_all.status_code == 200

    apartment_id = request_sale.json()['id']

    files_edit = [
        ('files', ('test.jpg', open('tests/templates/test.jpg', 'rb'), 'image/jpg')),
    ]
    request_sale_edit_not_found = client.put(
        f'{GET_APARTMENT_SALE}/0',
        data=EDITED_MOCKED_APARTMENT_SALE,
        headers={'Authorization': payload},
        files=files_edit,
    )

    assert request_sale_edit_not_found.status_code == 404
    assert request_sale_edit_not_found.json()['detail'] == 'Apartment is not found'

    request_sale_edit_image = client.put(
        f'{GET_APARTMENT_SALE}/{apartment_id}',
        data=EDITED_MOCKED_APARTMENT_SALE,
        headers={'Authorization': payload},
        files=files_edit,
    )
    assert request_sale_edit_image.json()['image'] == '{templates/images/test.jpg}'

    request_not_found = client.get(
        f'{GET_APARTMENT_SALE}/0',
        headers={'Authorization': payload},
    )

    assert request_not_found.status_code == 404
    assert request_not_found.json()['detail'] == 'Apartment is not found'

    request_view_apartment = client.get(
        f'{GET_APARTMENT_SALE}/{apartment_id}',
        headers={'Authorization': payload},
    )
    assert request_view_apartment.status_code == 200

    request_delete_apartment = client.delete(
        f'{GET_APARTMENT_SALE}/{apartment_id}',
        headers={'Authorization': payload},
    )
    assert request_delete_apartment.status_code == 204


# User check if rent apartment is created
def test__apartment_rent(client: TestClient):
    # given
    payload = _basic_auth_str(TEST_EMAIL, TEST_PASSWORD)
    files = [
        ('files', ('apartment.png', open('tests/templates/apartment.png', 'rb'), 'image/png')),
    ]

    # when
    request_rent = client.post(
        CREATE_APARTMENT_RENT,
        data=MOCKED_APARTMENT_RENT,
        headers={'Authorization': payload},
        files=files,
    )

    # then
    assert request_rent.status_code == 201
    assert request_rent.json()['living_area'] == 123
    assert request_rent.json()['number_of_bedrooms'] == 2
    assert request_rent.json()['number_of_bathrooms'] == 2
    assert request_rent.json()['condition'] == 'good'
    assert request_rent.json()['energy_label'] == 'a'
    assert request_rent.json()['building_year'] == 1996
    assert request_rent.json()['latitude'] == 40.151
    assert request_rent.json()['longitude'] == 44.516
    assert request_rent.json()['address'] == 'Erebuni, Yerevan, street Muratsan'
    assert request_rent.json()['rent_price'] == 123
    assert request_rent.json()['image'] == '{templates/images/apartment.png}'

    request_not_found = client.get(
        f'{GET_APARTMENT_RENT}/0',
        headers={'Authorization': payload},
    )

    assert request_not_found.status_code == 404
    assert request_not_found.json()['detail'] == 'Apartment is not found'

    request_show_all = client.get(
        GET_APARTMENT_RENT_QUERY,
        headers={'Authorization': payload},
    )
    assert request_show_all.status_code == 200

    apartment_id = request_rent.json()['id']

    files_edit = [
        ('files', ('test.jpg', open('tests/templates/test.jpg', 'rb'), 'image/jpg')),
    ]
    request_rent_edit_not_found = client.put(
        f'{GET_APARTMENT_RENT}/0',
        data=EDITED_MOCKED_APARTMENT_RENT,
        headers={'Authorization': payload},
        files=files_edit,
    )

    assert request_rent_edit_not_found.status_code == 404
    assert request_rent_edit_not_found.json()['detail'] == 'Apartment is not found'

    request_rent_edit_image = client.put(
        f'{GET_APARTMENT_RENT}/{apartment_id}',
        data=EDITED_MOCKED_APARTMENT_RENT,
        headers={'Authorization': payload},
        files=files_edit,
    )
    assert request_rent_edit_image.json()['image'] == '{templates/images/test.jpg}'

    request_not_found = client.get(
        f'{GET_APARTMENT_RENT}/0',
        headers={'Authorization': payload},
    )

    assert request_not_found.status_code == 404
    assert request_not_found.json()['detail'] == 'Apartment is not found'

    request_view_apartment = client.get(
        f'{GET_APARTMENT_RENT}/{apartment_id}',
        headers={'Authorization': payload},
    )
    assert request_view_apartment.status_code == 200

    request_delete_apartment = client.delete(
        f'{GET_APARTMENT_RENT}/{apartment_id}',
        headers={'Authorization': payload},
    )
    assert request_delete_apartment.status_code == 204


@pytest.mark.parametrize('model', [ApartmentSale, ApartmentRent])
def test_get_all_apartment(model):
    # Call the function to get all apartments
    result = get_all_apartment(model)

    # Perform assertions on the result
    # For example, you can check if the result is a valid SQLAlchemy select statement
    assert isinstance(result, sqlalchemy.Select)
