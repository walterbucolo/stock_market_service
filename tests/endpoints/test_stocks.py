from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from stock_market_app.main import app
from stock_market_app.services.auth_service import AuthService

client = TestClient(app)

# Overrides validate_api_key dependency
mock_validate_key = MagicMock()
def get_mock_validate_api_key():  # noqa: E302
    return mock_validate_key
app.dependency_overrides[AuthService.validate_api_key] = get_mock_validate_api_key  # noqa: E305


@patch('stock_market_app.endpoints.stocks.StockMarketService.get_stock_market_info', autospec=True)
def test_get_stocks_succesfully(mock_stock_market_service):
    expected_response = {
        'symbol': 'META',
        'open_price': "2",
        'higher_price': "3",
        'lower_price': "1",
        'variation': "0,5",
    }
    mock_stock_market_service.return_value = expected_response

    response = client.get("/api/stocks/meta")

    assert response.status_code == 200
    assert response.json() == expected_response


@patch('stock_market_app.endpoints.stocks.StockMarketService.get_stock_market_info', autospec=True)
def test_get_stocks_fails_when_symbol_is_not_valid(mock_stock_market_service):
    mock_stock_market_service.side_effect = HTTPException(status_code=404)

    response = client.get("/api/stocks/meta")

    assert response.status_code == 404


def test_get_stocks_fails_when_api_key_is_not_valid():
    app.dependency_overrides.clear()
    headers = {'api_key': 'fake_api_key'}

    response = client.get("/api/stocks/meta", headers=headers)

    assert response.status_code == 401
