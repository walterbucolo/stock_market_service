import logging 
from fastapi import FastAPI, Request

def log_request(app:FastAPI):
    # Set up loggings
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Outgoing response: {response.status_code}")
        return response
