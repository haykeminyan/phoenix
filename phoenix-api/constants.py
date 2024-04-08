ROOT_APP = 'phoenix-api/phoenix'
CREATE_USER_URL = 'http://127.0.0.1:8000/create_user'
TEST_EMAIL = 'admin@gmail.com'
TEST_PASSWORD = '@#$%Rewtegmfwep1!&$^'
ZERO_CREDITS = 0
IS_ACTIVE = True
IS_BANNED = not IS_ACTIVE
MILLION_CREDITS = 1000000
LIST_USERS = 'http://127.0.0.1:8000/users'
FAKE_EMAIL = 'lol@gmail.com'
FAKE_PASSWORD = '@#$%WEewtegmfwep1!&$^'
BAD_EMAIL = '123@'
BAD_PASSWORD = '123'
TEST_LOGIN = 'http://127.0.0.1:8000/admin/login'
TEST_LOGOUT = 'http://127.0.0.1:8000/admin/logout'
GET_APARTMENT_RENT = 'http://localhost:8000/apartment-rent'
GET_APARTMENT_RENT_QUERY = 'http://localhost:8000/apartment-rent?living_area=123&page=1'
GET_APARTMENT_SALE = 'http://localhost:8000/apartment-sale'
GET_APARTMENT_SALE_QUERY = 'http://localhost:8000/apartment-sale?living_area=123&page=1'
CREATE_APARTMENT_RENT = 'http://127.0.0.1:8000/apartment-rent/'
CREATE_APARTMENT_SALE = 'http://127.0.0.1:8000/apartment-sale/'
SALE_PATH_TEMPLATE = 'templates/sale_templates/sale.docx'
SALE_PATH_OUTPUT_TEMPLATE = 'templates/sale_output/Apartment Sale number.docx'
RENT_PATH_TEMPLATE = 'templates/rent_templates/rent.docx'
RENT_PATH_OUTPUT_TEMPLATE = 'templates/rent_output/Apartment Rent number.docx'
BAD_FIELDS_APARTMENT_RENT = ['sale_price']
BAD_FIELDS_APARTMENT_SALE = ['rent_price']
