from fastapi import HTTPException
import requests

from ..schemas import Stock
from ..constants import VANTAGE_DOMAIN
from ..helpers.settings import Settings
from ..helpers.logs_settings import get_logger

settings = Settings()
logger = get_logger()


class StockMarketService:

    def __init__(self, symbol, function='TIME_SERIES_DAILY_ADJUSTED') -> None:
        self.symbol = symbol
        self.function = function

    def get_stock_market_info(self):
        result = self.get_stock_market_info_from_vantage()
        if result.json().get('Error Message', None):
            raise HTTPException(status_code=404, detail="Not Found")

        try:
            time_series_daily = result.json().get('Time Series (Daily)')
            last_two_days = list(time_series_daily)[:2]
            last_day_close = float(time_series_daily[last_two_days[0]]['4. close'])
            before_last_day_close = float(time_series_daily[last_two_days[1]]['4. close'])
            variation = last_day_close - before_last_day_close
        except KeyError as exc:
            logger.error("Failed to manipulate data from vantage API. exc: {}".format(exc))
            raise exc

        return Stock(
            symbol=self.symbol,
            open_price=time_series_daily[last_two_days[0]]['1. open'],
            higher_price=time_series_daily[last_two_days[0]]['2. high'],
            lower_price=time_series_daily[last_two_days[0]]['3. low'],
            variation=round(variation, 3),
        )

    def get_stock_market_info_from_vantage(self):
        url = self.get_url()
        try:
            result = requests.get(url)
        except requests.exceptions.HTTPError as exc:
            logger.error("Request failed with error code {}".format(exc.response.status_code))
            raise exc
        except requests.exceptions.RequestException as exc:
            logger.error("Request failed with error {}".format(exc))
            raise exc
        return result

    def get_url(self):
        return VANTAGE_DOMAIN.format(
            function=self.function,
            symbol=self.symbol,
            api_key=settings.vantage_apikey
        )
