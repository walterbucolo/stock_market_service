from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from ..helpers.logs_settings import get_logger
from ..helpers.database import get_db
from ..services.user_service import UserService
from .. import schemas

router = APIRouter(tags=["users"])
logger = get_logger()


@router.post("/users", response_model=schemas.UserCreateResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        response = UserService(
            user.name,
            user.lastname,
            user.email,
            user.password,
            db
        ).create_user_with_api_key()
    except IntegrityError:
        error_msg = "User already exists with email {}".format(user.email)
        logger.error(msg=error_msg)

        raise HTTPException(
            status_code=409,
            detail=error_msg
        )

    return response
