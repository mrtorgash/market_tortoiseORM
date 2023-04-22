from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Field = для прописания ограничений сразу
class UserIn(BaseModel):
    username: str = Field(max_length=20, min_length=3)
    password: str = Field(max_length=20,
                          min_length=3)  # regex="^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){8,16}$") #


class UserId(BaseModel):
    id: int = Field()


class SuccessfulResponse(BaseModel):
    message: str = Field("Success")

class BadPriceResponse(BaseModel):
    message: str = Field("Bad price")

class TokenOut(BaseModel):
    token: str


class TokenData(BaseModel):
    username: str
    exp: Optional[datetime]
