from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from .helpers.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    api_key = relationship("APIKey", uselist=False, back_populates="user")


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="api_key")
