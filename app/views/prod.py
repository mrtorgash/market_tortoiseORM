from fastapi import Form
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import validator


class ProdPrice(BaseModel):
    price_from: int = Field()
    price_to: int = Field()

class ProdIn(BaseModel):
    prodname: str = Form(max_length=20, min_length=3)
    price: int = Form()



class ProdOut(BaseModel):
    id: int = Field()
    name: str = Field()
    price: int = Field()
    foto_loc: Optional[str]
    @validator("foto_loc")
    def assamble_foto_loc(cls, value: Optional[str]) -> Optional[str]:
       if value is not None and "static" not in value:
           return "/static/" + value
       return value




class ProdId(BaseModel):
    id : int = Field()

class ProdSearch(BaseModel):
    name: Optional[str] = Field()
    price: Optional[ProdPrice] = Field()
    @validator("price",pre=True)
    def assamble_price(cls, price: Optional[ProdPrice]) -> Optional[ProdPrice]:
        print("+++++++++++++")
        if price is not None:
            return price
        else:
            price: ProdPrice = ProdPrice(price_from=None, price_to=None)
            print(price)
            return price



