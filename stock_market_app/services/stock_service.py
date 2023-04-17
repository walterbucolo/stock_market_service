from fastapi import HTTPException
import requests
from ..schemas import Stock
from ..constants import VANTAGE_DOMAIN
from ..helpers.settings import Settings

settings = Settings()


class StockMarketService:

    def __init__(self, symbol, function='TIME_SERIES_DAILY_ADJUSTED') -> None:
        self.symbol = symbol
        self.function = function

    def get_stock_market_info(self):
        result = self.get_stock_market_info_from_vantage()
        if result.json().get('Error Message', None):
            raise HTTPException(status_code=404, detail="Not Found")

        time_series_daily = result.json().get('Time Series (Daily)')
        
        try:
            last_two_days = list(time_series_daily)[:2]
            last_day_close = float(time_series_daily[last_two_days[0]]['4. close'])
            before_last_day_close = float(time_series_daily[last_two_days[1]]['4. close'])
            variation = last_day_close - before_last_day_close
        except Exception:
            raise
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
        except Exception:
            raise  # TODO to handle this error properly

        return result

    def get_url(self):
        return VANTAGE_DOMAIN.format(
            function=self.function,
            symbol=self.symbol,
            api_key=settings.vantage_apikey
        )
