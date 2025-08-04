import aiomysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class AsyncDatabase:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        self.pool = await aiomysql.create_pool(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            autocommit=True,
            minsize=1,
            maxsize=10
        )

    async def query(self, sql, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
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
