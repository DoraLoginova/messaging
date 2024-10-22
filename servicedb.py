import asyncio
import aiopg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base
from typing import AsyncGenerator

DB_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"

engine = create_async_engine(DB_URL, echo=True, future=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def wait_for_db():
    for _ in range(5):
        try:
            async with aiopg.connect(
                dbname='postgres',
                user='postgres',
                password='postgres',
                host='db',
                port='5432'
            ):
                print("БД готова")
                return
        except Exception as e:
            print(f"Не удалось подключиться к БД: {e}")
            await asyncio.sleep(5)
    raise Exception("PostgreSQL не доступен.")


async def connect_db() -> AsyncGenerator[AsyncSession, None]:
    await wait_for_db()
    db = SessionLocal() 
    try:
        yield db 
    finally:
        await db.close()


# Создание таблиц
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
