from fastapi import APIRouter, Header, Depends, HTTPException
# from app.queries.auth import add_prod_to_db, get_prod_from_db
from tortoise.contrib.fastapi import HTTPNotFoundError

from app.auth.jwt_token import get_user, decode_token
from app.exceptions import UnAuthorized, ForbiddenError, InternalServerError, NotFoundError
from app.views.auth import SuccessfulResponse, UserId
from app.views.prod import ProdIn, ProdId, ProdOut
from app.views.auth import UserIn
from app.queries.follow import add_follow_to_db, viewing_follow, delete_follow_from_db
from typing import List
from app.views import from_list_to_pydantic
from app.views.tortoise_model import Users, Products, Prod_Pydantic

follow_router = APIRouter(tags=['Follow product'])


@follow_router.post('/add_follow_product', response_model=SuccessfulResponse)
async def add_follow_prod(prod_id: ProdId, token: str = Header()):
    token = decode_token(token)
    user = await Users.get(username = token.username)
    prod = await Products.get(id = prod_id.id)
    await user.follow.add(prod)
    return SuccessfulResponse()


@follow_router.get("/viewing_follow", response_model=List[Prod_Pydantic])
async def view_follow_prod(token : str = Header()):
    token = decode_token(token)
    user = await Users.get(username = token.username)
    prod = user.follow.all()
    return await Prod_Pydantic.from_queryset(prod)

@follow_router.delete("/delete_follow", response_model=SuccessfulResponse)
async def delete_follow_prod(prod_id: ProdId, token: str = Header()):
    token = decode_token(token)
    user = await Users.get(username = token.username)
    prod = await Products.get(id = prod_id.id)
    await user.follow.remove(prod)
    return SuccessfulResponse()