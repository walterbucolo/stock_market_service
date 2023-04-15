from sqlalchemy.exc import IntegrityError
from fastapi.testclient import TestClient
from unittest.mock import patch
from stock_market_app.main import app
from stock_market_app.schemas import UserCreateResponse

client = TestClient(app)


@patch('stock_market_app.endpoints.users.UserService.create_user_with_api_key', autospec=True)
def test_create_users_succesfully(create_user_with_api_key):
    create_user_with_api_key.return_value = UserCreateResponse(
        id='1',
        name='Walt',
        lastname='Buc',
        email='fake@fake.com',
        api_key='fake_api_key',
    )

    response = client.post(
        "/api/users",
        json={"name": "Walt", "lastname": "Buc", "email": "fake@fake.com"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Walt",
        "lastname": "Buc",
        "email": "fake@fake.com",
        "api_key": "fake_api_key",
    }


def test_create_users_fails_when_param_is_missing():
    response = client.post(
        "/api/users",
        json={"lastname": "Buc", "email": "fake@fake.com"}
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'field required'
    assert response.json()['detail'][0]['loc'][1] == 'name'


@patch('stock_market_app.endpoints.users.UserService.create_user_with_api_key')
def test_create_users_fails_when_email_already_exists(create_user_with_api_key):
    email = "fake@fake.com"
    create_user_with_api_key.side_effect = IntegrityError(
        statement='INSERT INTO users (name, lastname, email) VALUES (?, ?, ?)',
        params=('Walt', 'Buc', email),
        orig=None,
    )

    # with pytest.raises(IntegrityError) as exc:
    response = client.post(
        "/api/users",
        json={"name": "Walt", "lastname": "Buc", "email": email}
    )

    assert response.status_code == 409
    assert response.json()['detail'] == 'User already exists with email {}'.format(email)
