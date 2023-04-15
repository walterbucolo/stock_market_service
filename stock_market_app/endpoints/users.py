from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..helpers.database import get_db
from ..services.user_service import UserService
from .. import schemas

router = APIRouter(tags=["users"])


@router.post("/users", response_model=schemas.UserCreateResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        response = UserService(user.name, user.lastname, user.email, db).create_user_with_api_key()
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="User already exists with email {}".format(user.email)
        )

    return response
