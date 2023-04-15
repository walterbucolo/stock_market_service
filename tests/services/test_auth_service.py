import pytest
from unittest.mock import MagicMock, patch
from stock_market_app.models import APIKey
from stock_market_app.services.auth_service import AuthService
import re
from fastapi import HTTPException, Request


class TestAuthService:

    @patch.object(AuthService, 'save_api_key', return_value=APIKey())
    def test_create_api_key_successfully(self, mock_api_key_object):
        db = MagicMock()
        auth_service = AuthService(user_id=1, db=db)

        with patch.object(AuthService, "generate_api_key", return_value="fake_api_key") as mock_generate_api_key:
            with patch.object(AuthService, "hash_api_key", return_value="hashed_api_key") as mock_hash_api_key:
                api_key = auth_service.create_api_key()

        mock_generate_api_key.assert_called_once()
        mock_hash_api_key.assert_called_once_with("fake_api_key")
        mock_api_key_object.assert_called_once_with("hashed_api_key")
        assert api_key == "fake_api_key"

    def test_hash_api_key_successfully(self):
        api_key = AuthService.generate_api_key()
        pattern = re.compile(r'^[0-9a-f]+$')  # Returned key should consists only of hexadecimal digits (0-9, a-f).

        hashed_api_key = AuthService.hash_api_key(api_key)

        assert pattern.match(hashed_api_key)
        assert type(hashed_api_key) == str
        assert len(hashed_api_key) == 64

    def test_save_api_key_successfully(self):
        db = MagicMock()
        auth_service = AuthService(user_id=1, db=db)

        db_api_key = auth_service.save_api_key(api_key_hashed="hashed_api_key")

        db.add.assert_called_once_with(db_api_key)
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(db_api_key)
        assert db_api_key

    @patch.object(AuthService, 'get_api_key')
    def test_validate_api_key_successfully(self, mock_get_api_key):
        db = MagicMock()
        fake_api_key = 'fake_api_key'
        hashed_api_key = 'fake_api_key'
        mock_get_api_key.return_value = APIKey(key=fake_api_key)
        request: Request = MagicMock()
        request.headers = {'Api-key': fake_api_key}

        with patch.object(AuthService, "hash_api_key", return_value=hashed_api_key) as mock_hash_api_key:
            AuthService.validate_api_key(request=request, db=db)

        mock_hash_api_key.assert_called_once_with(fake_api_key)
        mock_get_api_key.assert_called_once_with(db, hashed_api_key)

    @patch.object(AuthService, 'get_api_key')
    def test_validate_api_key_fails_when_api_is_not_found(self, mock_get_api_key):
        db = MagicMock()
        fake_api_key = 'fake_api_key'
        hashed_api_key = 'fake_api_key'
        mock_get_api_key.return_value = []  # api_key was not found
        request: Request = MagicMock()
        request.headers = {'Api-key': fake_api_key}

        with patch.object(AuthService, "hash_api_key", return_value=hashed_api_key) as mock_hash_api_key:
            with pytest.raises(HTTPException):
                AuthService.validate_api_key(request=request, db=db)

        mock_hash_api_key.assert_called_once_with(fake_api_key)
        mock_get_api_key.assert_called_once_with(db, hashed_api_key)
