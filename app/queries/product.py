from app.servecise.database import DB
from app.exceptions import BadRequestError, NotFoundError
# from asyncpg.types import Record
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from typing import Optional


async def add_prod_to_db(name: str, price: int, file_path: Optional[str]) -> None:
    sql = """
        insert into product(name,price,foto_loc)
        values ($1,$2,$3)
    """
    async with DB.pool.acquire() as conn:
        try:
            await conn.execute(sql, name, price, file_path)
        except UniqueViolationError as e:
            raise BadRequestError(message="prodname already exist") from e


async def search_prod_from_db(prodname: str, price_from: int, price_to: int):  # name+  / name, price / price
    if prodname is not None and price_from is not None and price_to is not None:
        sql = """
                select * from product
                where name ILIKE $1 and
                price > $2 and price < $3            
            """
        # where name LIKE concat( $1,'%')
        async with DB.pool.acquire() as conn:
            result = await conn.fetch(sql, prodname, price_from, price_to)
            return result
    elif prodname is not None:
        sql = """
            select * from product
            where name ILIKE $1
        """

        async with DB.pool.acquire() as conn:
            result = await conn.fetch(sql, prodname)
            return result
    elif price_from is not None:
        sql = """
            select * from product
            where price > $1 and price < $2
        """
        async with DB.pool.acquire() as conn:
            result = await conn.fetch(sql, price_from, price_to)
            return result


async def viewing_prod() -> list:
    sql = """
        select * from product
    """
    async with DB.pool.acquire() as conn:
        result = await conn.fetch(sql)
        return result


async def delete_prod_from_db(prod_id: int):
    sql = """
        delete from product
        where id = $1
    """
    async with DB.pool.acquire() as conn:
        try:
            await conn.execute(sql, prod_id)
        except ForeignKeyViolationError as e:
            raise NotFoundError(message="Товара нет") from e

# async def search_prod_from_db(prodname: str,price_from: int,price_to:int): # name+  / name, price / price
#    if prodname is not None and price_from is not None and price_to is not None:
#        sql = """
#                select * from product
#                where name = coalesce($1, name) and
#            price > $2 and price < $3
#           """
#        async with DB.pool.acquire() as conn:
#    result = await conn.fetch(sql, prodname,price_from,price_to)
#    return result
# elif prodname is not None:
# sql = """
#   select * from product
#   where name = coalesce($1,name)
# """
# async with DB.pool.acquire() as conn:
#    result = await conn.fetch(sql, prodname)
#    return result
# elif price_from is not None:
#    sql = """
#       select * from product
#    where price > $1 and price < $2
# """
# async with DB.pool.acquire() as conn:
#     result = await conn.fetch(sql, price_from,price_to)
#    return result
