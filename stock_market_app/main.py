from fastapi import FastAPI
from .helpers import database
from .helpers.logs_settings import get_logger
from fastapi import Request
from .endpoints import users, stocks

database.Base.metadata.create_all(bind=database.engine)

logger = get_logger()

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Outgoing response: {response.status_code}")
    return response


app.include_router(users.router, prefix="/api")
app.include_router(stocks.router, prefix="/api")
