import asyncio
import asyncpg
from typing import Any, Protocol

# Определяем интерфейсы с помощью протоколов
class Creator(Protocol):
    async def create(self, conn: asyncpg.Connection) -> int:
        ...

class Reader(Protocol):
    async def read(self, conn: asyncpg.Connection) -> Any:
        ...

class Updater(Protocol):
    async def update(self, conn: asyncpg.Connection) -> None:
        ...

class Deleter(Protocol):
    async def delete(self, conn: asyncpg.Connection) -> None:
        ...

class Database:
    def __init__(self, db_url: str, timeout: int = 3):
        self.db_url = db_url
        self.timeout = timeout
        self.pool: asyncpg.Pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.db_url)

    async def close(self):
        await self.pool.close()

    async def read(self, reader: Reader) -> Any:
        async with self.pool.acquire() as conn:
            return await reader.read(conn)

    async def create(self, creator: Creator) -> int:
        async with self.pool.acquire() as conn:
            return await creator.create(conn)

    async def update(self, updater: Updater) -> None:
        async with self.pool.acquire() as conn:
            await updater.update(conn)

    async def delete(self, deleter: Deleter) -> None:
        async with self.pool.acquire() as conn:
            await deleter.delete(conn)

# Пример использования базы данных
async def main():
    db = Database('postgresql://user:password@localhost/dbname')
    await db.connect()

    # Пример создания, чтения, обновления и удаления данных
    # await db.create(your_creator_instance)
    # await db.read(your_reader_instance)
    # await db.update(your_updater_instance)
    # await db.delete(your_deleter_instance)

    await db.close()

# Запуск основного цикла
if __name__ == '__main__':
    asyncio.run(main())
