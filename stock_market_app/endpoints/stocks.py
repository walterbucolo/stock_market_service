from fastapi import APIRouter, Depends, HTTPException
import requests

from ..schemas import Stock
from ..services.stock_service import StockMarketService
from ..services.auth_service import AuthService

router = APIRouter(tags=["stocks"], dependencies=[Depends(AuthService.validate_api_key)])


@router.get("/stocks/{symbol}", response_model=Stock)
def get_stocks(symbol):
    try:
        return StockMarketService(symbol=symbol).get_stock_market_info()
    except (
        requests.exceptions.RequestException,
        requests.exceptions.HTTPError,
        KeyError,
    ):
        raise HTTPException(status_code=502, detail="Error retrieving stock information.")

