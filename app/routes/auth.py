from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from app.auth.jwt_token import create_access_token
from app.queries.auth import add_user_to_db, get_user_from_db
from fastapi.exceptions import HTTPException
from fastapi import status
from app.exceptions import UnAuthorized,ForbiddenError,InternalServerError, NotFoundError
from app.auth.hash import get_password_hash, verify_password
from app.views.auth import UserIn, SuccessfulResponse, TokenOut, TokenData
from app.views.tortoise_model import Users,User_Pydantic,UserIn_Pydantic
from typing import List

auth_router = APIRouter(tags=['Authentication'])



@auth_router.post("/register", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    user_obj.password = get_password_hash(user_obj.password)
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@auth_router.get("/users", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())

@auth_router.get("/user", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_user(user_id: int):
    print(Users.all().sql())  #проверка запроса
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))

@auth_router.post('/login',response_model=TokenOut)
async def login_user(user_in: UserIn_Pydantic):

    print(Users.get(username = user_in.username).sql())
    user_obj = await Users.get(username = user_in.username)#get_user_from_db(user_in.username)
    print("+++++++++++++++")
    if not user_obj:
        raise NotFoundError(message="Username not found")
    if not verify_password(user_in.password, user_obj.password):
        return SuccessfulResponse()
    token_data = TokenData(username = user_obj.username)
    access_token = create_access_token(token_data)
    return TokenOut(token = access_token)

