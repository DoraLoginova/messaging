import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_LIFE = os.getenv("TOKEN_LIFE")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register_user(username, password, db):
    exist_user = await db.execute(
        select(User).where(User.username == username)
    )
    if exist_user.scalars().first():
        return False
    hash_password = pwd_context.hash(password)
    await db.execute(User.__table__.insert().values(
        username=username,
        password=hash_password
    ))
    return True


async def login_user(db, username, password):
    res = await db.execute(select(User).where(User.username == username))
    user = res.scalars().first()
    if not user or not pwd_context.verify(password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )
    token_data = {"sub": user.username}
    expiration = datetime.now() + timedelta(minutes=TOKEN_LIFE)
    token_data.update({"exp": expiration})
    access_token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}
