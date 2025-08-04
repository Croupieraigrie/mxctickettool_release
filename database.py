import aiomysql
from bot.config import Config

class AsyncDatabase:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        self.pool = await aiomysql.create_pool(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            db=Config.DB_NAME,
            autocommit=True,
            minsize=1,
            maxsize=10,
        )

    async def query(self, sql, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, params or ())
                result = await cur.fetchall()
                return result

    async def execute(self, sql, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, params or ())
                return cur.lastrowid

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()

db = AsyncDatabase()
