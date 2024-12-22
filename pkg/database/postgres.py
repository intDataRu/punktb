import asyncio
from asyncpg import Pool, Connection
from typing import Protocol, Any

# Константа для таймаута
TIMEOUT = 3

# Определяем интерфейсы для операций с базой данных
class Creator(Protocol):
    async def create(self, conn: Connection) -> int:
        ...

class Reader(Protocol):
    async def read(self, conn: Connection) -> Any:
        ...

class Updater(Protocol):
    async def update(self, conn: Connection) -> None:
        ...

class Deleter(Protocol):
    async def delete(self, conn: Connection) -> None:
        ...

class Database(Protocol):
    async def create(self, i: Creator) -> int:
        ...

    async def read(self, i: Reader) -> Any:
        ...

    async def update(self, i: Updater) -> None:
        ...

    async def delete(self, i: Deleter) -> None:
        ...

# Реализация PostgreSQL базы данных
class Postgres:
    def __init__(self, pool: Pool):
        self.pool = pool

    @classmethod
    async def new_database(cls, db_url: str) -> 'Postgres':
        pool = await asyncpg.create_pool(dsn=db_url)
        return cls(pool)

    async def read(self, i: Reader) -> Any:
        async with self.pool.acquire() as conn:
            return await i.read(conn)

    async def create(self, i: Creator) -> int:
        async with self.pool.acquire() as conn:
            return await i.create(conn)

    async def update(self, i: Updater) -> None:
        async with self.pool.acquire() as conn:
            await i.update(conn)

    async def delete(self, i: Deleter) -> None:
        async with self.pool.acquire() as conn:
            await i.delete(conn)
