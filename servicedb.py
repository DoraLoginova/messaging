import os
import asyncio
import aiopg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

from models import Base

load_dotenv()

DB = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


engine = create_engine(DB, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def wait_for_db():
    for _ in range(5):
        try:
            async with aiopg.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            ):
                print("БД готова")
                return
        except Exception as e:
            print(f"Не удалось подключиться к БД: {e}")
            await asyncio.sleep(5)
    raise Exception("PostgreSQL не доступен.")


async def connect_db() -> Session:
    await wait_for_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
