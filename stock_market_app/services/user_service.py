from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from stock_market_app.schemas import UserCreateResponse
from stock_market_app.services.auth_service import AuthService
from ..models import User


class UserServiceBase:
    def __init__(self, name: str, lastname: str, email: str, password: str) -> None:
        self.name = name
        self.lastname = lastname
        self.password = password
        self.email = email


class UserService(UserServiceBase):
    def __init__(self, name: str, lastname: str, email: str, password: str, db: Session) -> None:
        self.db = db
        super().__init__(name, lastname, email, password)

    def create_user(self):
        hashed_password = bcrypt.hash(self.password)
        db_user = User(name=self.name, lastname=self.lastname, email=self.email, hashed_password=hashed_password)
        self.db.add(db_user)
        try:
            self.db.commit()
        except IntegrityError as exc:
            raise exc
        self.db.refresh(db_user)
        return db_user

    def create_user_with_api_key(self):
        user = self.create_user()
        api_key = AuthService(user.id, self.db).create_api_key()
        return UserCreateResponse(
            id=user.id,
            name=user.name,
            lastname=user.lastname,
            email=user.email,
            api_key=api_key,
        )
