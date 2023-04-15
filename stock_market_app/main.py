from fastapi import FastAPI
from .endpoints import users, stocks
from .helpers import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(users.router, prefix="/api")
app.include_router(stocks.router, prefix="/api")
