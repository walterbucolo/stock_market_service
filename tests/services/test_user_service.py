from sqlite3 import IntegrityError
from unittest.mock import MagicMock, patch

import pytest
from stock_market_app.models import User
from stock_market_app.schemas import UserCreateResponse
from stock_market_app.services.auth_service import AuthService
from stock_market_app.services.user_service import UserService


class TestUserService:
    def test_create_user_successfully(self):
        db = MagicMock()
        user_service = UserService(
            name="John",
            lastname="Lennon",
            email="lennonjohn@fake.com",
            password="passw",
            db=db)

        db_user = user_service.create_user()

        db.add.assert_called_once_with(db_user)
        db.commit.assert_called_once_with()
        db.refresh.assert_called_once_with(db_user)
        assert db_user.name == "John"
        assert db_user.lastname == "Lennon"
        assert db_user.email == "lennonjohn@fake.com"

    def test_create_user_fails_when_user_already_exist(self):
        db = MagicMock()
        db.commit.side_effect = IntegrityError()

        user_service = UserService(
            name="John",
            lastname="Lennon",
            email="lennonjohn@fake.com",
            password="passw",
            db=db)

        with pytest.raises(IntegrityError):
            user_service.create_user()

    @patch.object(UserService, 'create_user')
    @patch.object(AuthService, 'create_api_key')
    def test_create_user_with_api_key(self, mock_create_api_key, mock_create_user):
        db = MagicMock()
        user_service = UserService(
            name="John",
            lastname="Lennon",
            email="lennonjohn@fake.com",
            password="passw",
            db=db)
        mock_create_user.return_value = User(
            id=1,
            name="John",
            lastname="Lennon",
            email="lennonjohn@fake.com"
        )
        mock_create_api_key.return_value = "fake_api_key"

        response = user_service.create_user_with_api_key()

        mock_create_user.assert_called_once_with()
        mock_create_api_key.assert_called_once_with()
        assert response == UserCreateResponse(
            id=1,
            name="John",
            lastname="Lennon",
            email="lennonjohn@fake.com",
            api_key="fake_api_key",
        )
