from fastapi import FastAPI

from stock_market_app.middlewares.logging import log_request
from .endpoints import users, stocks
from .helpers import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
log_request(app)

app.include_router(users.router, prefix="/api")
app.include_router(stocks.router, prefix="/api")
