from pydantic import EmailStr, BaseModel


class UserBase(BaseModel):
    name: str
    lastname: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserCreateResponse(UserBase):
    id: int
    api_key: str


class Stock(BaseModel):
    symbol: str
    open_price: str
    higher_price: str
    lower_price: str
    variation: str
