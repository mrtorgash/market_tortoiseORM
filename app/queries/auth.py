from app.servecise.database import DB
from app.exceptions import BadRequestError
# from asyncpg.types import Record
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError  # 1 если запись
# с полем которое есть уже есть 2 сслылается на несуществующую запись другой таблицы

async def add_user_to_db(username: str, password: str) -> None:
    sql = """
       insert  into users (username,password)
       values ($1,$2)
    """
    async with DB.pool.acquire() as conn:
        try:
            await conn.execute(sql, username, password)
        except UniqueViolationError as e:
            raise BadRequestError(message="Username already exist") from e


async def get_user_from_db(username: str):  # -> Record тут должен быть Record
    # Record - словарь из значений базы данных
    sql = """
        select username,password from users
        where username = $1
        """
    async with DB.pool.acquire() as conn:
        result = await conn.fetchrow(sql, username)
        return result


