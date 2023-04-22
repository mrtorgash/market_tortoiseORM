import asyncpg
from app.confige import settings

class DB:
    pool: asyncpg.Pool = None

    @classmethod
    async def connect_db(cls):
        cls.pool = await asyncpg.create_pool(settings.DB_URL,max_inactive_connection_lifetime=100)


    @classmethod
    async def disconnect_db(cls):
        await cls.pool.close()
        postgres