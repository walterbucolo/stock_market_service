import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from stock_market_app.schemas import Stock
from stock_market_app.services.stock_service import StockMarketService
from stock_market_app.constants import VANTAGE_DOMAIN
from tests.helpers.mock_response_vantage_api import MOCK_RESPONSE_VANTAGE_API, MOCK_RESPONSE_VANTAGE_API_ERROR_NOT_FOUND


class TestStockMarketService:

    @patch('stock_market_app.services.stock_service.settings')
    def test_get_url(self, mock_settings):
        mock_settings.vantage_apikey = 'fake_vantage_apikey'
        stock_market_service = StockMarketService(symbol="meta")
        expected_url = VANTAGE_DOMAIN.format(
            function='TIME_SERIES_DAILY_ADJUSTED',
            symbol='mceta',
            api_key='fake_vantage_apikey'
        )

        url = stock_market_service.get_url()

        assert url == expected_url

    @patch.object(StockMarketService, 'get_stock_market_info_from_vantage')
    def test_get_stock_market_info_successfully(self, mock_stock_market_info_from_vantage):
        stock_market_service = StockMarketService(symbol="meta")
        fake_response = MagicMock()
        fake_response.json.return_value = MOCK_RESPONSE_VANTAGE_API
        mock_stock_market_info_from_vantage.return_value = fake_response

        response = stock_market_service.get_stock_market_info()

        assert response == Stock(
            symbol='meta',
            open_price='217.88',
            higher_price='222.11',
            lower_price='217.55',
            variation='1.14'
        )

    @patch.object(StockMarketService, 'get_stock_market_info_from_vantage')
    def test_get_stock_market_info_raise_when_error_in_api(self, mock_stock_market_info_from_vantage):
        stock_market_service = StockMarketService(symbol="fake")
        fake_response = MagicMock()
        fake_response.json.return_value = MOCK_RESPONSE_VANTAGE_API_ERROR_NOT_FOUND

        mock_stock_market_info_from_vantage.return_value = fake_response

        with pytest.raises(HTTPException):
            stock_market_service.get_stock_market_info()
