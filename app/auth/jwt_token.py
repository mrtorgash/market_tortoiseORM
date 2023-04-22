from datetime import datetime,timedelta
from typing import Optional
from jose import jwt, JWTError
from app.confige import settings
from app.servecise.database import DB
from app.views.auth import TokenData
from app.exceptions import UnAuthorized
from pydantic import ValidationError
from pytz import timezone

def create_access_token(data: TokenData) -> str:
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.exp = expire
    encoded_jwt = jwt.encode(dict(data), settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        token_data = TokenData(**payload)  #**kwargs время 20:51
        if datetime.now(timezone('Europe/Moscow')) > token_data.exp:
            raise UnAuthorized
        return token_data
    except JWTError as e:
        raise UnAuthorized from e
    except ValidationError as e:
        raise UnAuthorized from e

async def get_user(token: str) -> dict:
    token = decode_token(token)
    sql = """
        select * from users
        where username = $1
    """
    async with DB.pool.acquire() as conn:
        result = await conn.fetchrow(sql, token.username)
        return result