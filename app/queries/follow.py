from app.servecise.database import DB
from app.exceptions import BadRequestError, NotFoundError
# from asyncpg.types import Record
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError


async def add_follow_to_db(user_id: int, prod_id: int) ->  None:
    sql = """
        insert into follow(user_id,prod_id)
        values ($1,$2)
    """
    async with DB.pool.acquire() as conn:
        try:
            await conn.execute(sql, user_id, prod_id)
        except UniqueViolationError as e:
            raise BadRequestError(message="follow already exist") from e
        except ForeignKeyViolationError as f:
            raise NotFoundError(message=" товар не найден") from f
#делать по аналогии с верхним
async def viewing_follow(user_id: int) -> list:

    # нужен селект запрос обьединяющий 2 таблицы
    # мне нужно вывести по id пользовател вывести его любимые
    # продукты.   user_id -> prod_id -> id -> name
    #
    sql = """
        select id,name,price from product JOIN follow on prod_id = id 
        where user_id = $1
    """
    async with DB.pool.acquire() as conn:
        result = await conn.fetch(sql, user_id)
        return result

async def delete_follow_from_db(user_id: int, prod_id: int):
    sql = """
        delete from follow
        where user_id = $1 and prod_id = $2
    """
    async with DB.pool.acquire() as conn:
        try:
            await conn.execute(sql, user_id,prod_id)
        except ForeignKeyViolationError as e:
            raise NotFoundError(message="Товара нет") from e

#select * from product JOIN follow on prod_id = id where user_id = 1
#завтра удалить из избранного++++ + удалить товар из базы++++, если будет время то картинки